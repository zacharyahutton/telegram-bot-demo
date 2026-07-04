from __future__ import annotations

import logging
import random
import re
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.config import settings
from bot.content.brand import (
    ABOUT_TEXT,
    AI_MODE_TEXT,
    FAQ_MODE_TEXT,
    HELP_TEXT,
    MAIN_MENU_TEXT,
    PARSE_MODE,
    REVIEWER_TOUR_TEXT,
    SETTINGS_MODE_TEXT,
    TOOLS_MODE_TEXT,
    WELCOME_TEXT,
    confirmation_card,
    faq_answer,
    step_label,
)
from bot.content.faq import CATEGORY_INTROS, FAQ_ENTRIES, match_faq
from bot.database import db
from bot.keyboards.menus import (
    about_keyboard,
    booking_services_keyboard,
    booking_times_keyboard,
    faq_categories_keyboard,
    faq_category_items_keyboard,
    main_menu_keyboard,
    persistent_reply_keyboard,
    settings_keyboard,
    support_category_keyboard,
    support_priority_keyboard,
    tools_keyboard,
)
from bot.services.llm import chat_completion

logger = logging.getLogger(__name__)

# Booking conversation states
BOOK_SERVICE, BOOK_DATE, BOOK_TIME = range(3)
# Support ticket states
TICKET_CAT, TICKET_DESC, TICKET_PRI = range(3, 6)

TIPS = [
    "Use fallback handlers when users send unexpected input mid-flow.",
    "Log every webhook delivery and LLM failure for production debugging.",
    "Store conversation state in a database, not only in memory.",
    "Rate-limit per user to survive abuse and platform quotas.",
    "Keep AI replies short; offer human escalation for account-specific tasks.",
    "WhatsApp templates need approval; design proactive messages early.",
    "Sign outbound webhooks with HMAC so receivers trust your payloads.",
    "Test interactive buttons on mobile; thumb reach matters.",
]


async def _guard_rate(update: Update) -> bool:
    user = update.effective_user
    if not user:
        return False
    ok = await db.check_rate_limit(user.id)
    if not ok and update.effective_message:
        await update.effective_message.reply_text(
            "You are sending messages too quickly. Please wait a moment and try again.",
            parse_mode=PARSE_MODE,
        )
    return ok


async def _track(user_id: int | None, event: str, payload=None) -> None:
    await db.log_event(user_id, event, payload)


async def _reply_html(message, text: str, **kwargs) -> None:
    await message.reply_text(text, parse_mode=PARSE_MODE, **kwargs)


async def _edit_html(query, text: str, **kwargs) -> None:
    await query.edit_message_text(text, parse_mode=PARSE_MODE, **kwargs)


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    if not await _guard_rate(update):
        return
    user = update.effective_user
    await db.upsert_user(user.id, user.username, user.first_name)
    await db.set_mode(user.id, "menu")
    await _track(user.id, "start")
    await _reply_html(
        update.effective_message,
        WELCOME_TEXT,
        reply_markup=persistent_reply_keyboard(),
    )
    await _reply_html(update.effective_message, MAIN_MENU_TEXT, reply_markup=main_menu_keyboard())


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    if not await _guard_rate(update):
        return
    if update.effective_user:
        await db.set_mode(update.effective_user.id, "menu")
    await _reply_html(update.effective_message, MAIN_MENU_TEXT, reply_markup=main_menu_keyboard())


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    if update.effective_user:
        await _track(update.effective_user.id, "about")
    await _reply_html(update.effective_message, ABOUT_TEXT, reply_markup=about_keyboard())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    await _reply_html(update.effective_message, HELP_TEXT, reply_markup=main_menu_keyboard())


async def forget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    await db.clear_chat_history(update.effective_user.id)
    await _reply_html(
        update.effective_message,
        "<b>AI memory cleared</b>\n\nYour conversation history has been removed from this demo instance.",
    )


async def review_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    await _track(update.effective_user.id, "review_tour")
    await _reply_html(
        update.effective_message,
        REVIEWER_TOUR_TEXT,
        reply_markup=main_menu_keyboard(),
    )


async def health_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    llm = "configured" if settings.resolve_llm() else "not configured"
    mode = "webhook" if settings.webhook_url else "polling"
    await _reply_html(
        update.effective_message,
        confirmation_card(
            "Tendem Health Check",
            [
                f"Status: healthy",
                f"Mode: {mode}",
                f"LLM: {llm}",
                f"Database: {settings.database_path}",
                f"Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
            ],
        ),
    )


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    if update.effective_user.id not in settings.admin_ids:
        await _reply_html(update.effective_message, "Admin only.")
        return
    s = await db.stats()
    await _reply_html(
        update.effective_message,
        confirmation_card(
            "Admin Analytics",
            [
                f"Users: {s['users']}",
                f"Bookings: {s['bookings']}",
                f"Tickets: {s['tickets']}",
                f"Events logged: {s['events']}",
            ],
        ),
    )


async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    await db.set_mode(update.effective_user.id, "ai")
    await _reply_html(update.effective_message, AI_MODE_TEXT)


async def faq_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return
    await db.set_mode(update.effective_user.id, "faq")
    await _reply_html(
        update.effective_message,
        FAQ_MODE_TEXT,
        reply_markup=faq_categories_keyboard(),
    )


async def _show_menu(query) -> None:
    await _edit_html(query, MAIN_MENU_TEXT, reply_markup=main_menu_keyboard())


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    query = update.callback_query
    if not query or not query.data:
        return None
    await query.answer()
    data = query.data
    user = update.effective_user
    if not user:
        return None

    if data in ("menu", "nav:menu"):
        await db.set_mode(user.id, "menu")
        await _show_menu(query)
        return ConversationHandler.END

    if data.startswith("mode:"):
        mode = data.split(":", 1)[1]
        await db.set_mode(user.id, mode)
        await _track(user.id, "mode_select", {"mode": mode})
        if mode == "ai":
            await _edit_html(query, AI_MODE_TEXT, reply_markup=main_menu_keyboard())
        elif mode == "faq":
            await _edit_html(query, FAQ_MODE_TEXT, reply_markup=faq_categories_keyboard())
        elif mode == "book":
            await _edit_html(
                query,
                f"{step_label(1, 3, 'Select a service')}\n\nChoose the appointment type:",
                reply_markup=booking_services_keyboard(),
            )
            return BOOK_SERVICE
        elif mode == "support":
            await _edit_html(
                query,
                f"{step_label(1, 3, 'Ticket category')}\n\nWhat area do you need help with?",
                reply_markup=support_category_keyboard(),
            )
            return TICKET_CAT
        elif mode == "tools":
            await _edit_html(query, TOOLS_MODE_TEXT, reply_markup=tools_keyboard())
        elif mode == "settings":
            await _edit_html(query, SETTINGS_MODE_TEXT, reply_markup=settings_keyboard())
        elif mode == "about":
            await _track(user.id, "about")
            await _edit_html(query, ABOUT_TEXT, reply_markup=about_keyboard())
        elif mode == "review":
            await _track(user.id, "review_tour")
            await _edit_html(query, REVIEWER_TOUR_TEXT, reply_markup=main_menu_keyboard())
        return None

    if data.startswith("faqcat:"):
        cat = data.split(":", 1)[1]
        intro = CATEGORY_INTROS.get(cat, cat)
        await _edit_html(
            query,
            f"{intro}\n\n<b>Tap a topic:</b>",
            reply_markup=faq_category_items_keyboard(cat),
        )
        return None

    if data.startswith("faqidx:"):
        idx = int(data.split(":", 1)[1])
        if 0 <= idx < len(FAQ_ENTRIES):
            hit = FAQ_ENTRIES[idx]
            await _edit_html(
                query,
                faq_answer(hit["q"], hit["a"]),
                reply_markup=faq_category_items_keyboard(hit["cat"]),
            )
        return None

    if data.startswith("booksvc:"):
        context.user_data["book_service"] = data.split(":", 1)[1]
        await _edit_html(
            query,
            f"{step_label(2, 3, 'Pick a date')}\n\nEnter booking date as <code>YYYY-MM-DD</code>\n"
            "Example: <code>2026-07-15</code>",
        )
        return BOOK_DATE

    if data.startswith("booktime:"):
        context.user_data["book_time"] = data.split(":", 1)[1]
        service = context.user_data.get("book_service", "Service")
        bdate = context.user_data.get("book_date", "TBD")
        btime = context.user_data.get("book_time")
        bid = await db.create_booking(user.id, service, bdate, btime)
        await _track(user.id, "booking_created", {"id": bid})
        await _edit_html(
            query,
            confirmation_card(
                "Booking Confirmed",
                [
                    f"ID: #{bid}",
                    f"Service: {service}",
                    f"Date: {bdate}",
                    f"Time: {btime}",
                ],
                "A confirmation template would be sent in production (WhatsApp/Telegram).",
            ),
            reply_markup=main_menu_keyboard(),
        )
        context.user_data.clear()
        return ConversationHandler.END

    if data.startswith("ticketcat:"):
        context.user_data["ticket_cat"] = data.split(":", 1)[1]
        await _edit_html(
            query,
            f"{step_label(2, 3, 'Describe the issue')}\n\nSend one message with details:",
        )
        return TICKET_DESC

    if data.startswith("ticketpri:"):
        pri = data.split(":", 1)[1]
        desc = context.user_data.get("ticket_desc", "")
        cat = context.user_data.get("ticket_cat", "General")
        tid = await db.create_ticket(user.id, cat, desc, pri)
        await _track(user.id, "ticket_created", {"id": tid, "priority": pri})
        await _edit_html(
            query,
            confirmation_card(
                "Support Ticket Opened",
                [
                    f"Ticket ID: #{tid}",
                    f"Category: {cat}",
                    f"Priority: {pri.title()}",
                ],
                "A Tendem agent would pick this up in the hybrid queue.",
            ),
            reply_markup=main_menu_keyboard(),
        )
        context.user_data.clear()
        return ConversationHandler.END

    if data.startswith("tool:"):
        parts = data.split(":", 2)
        tool = parts[1]
        if tool == "tip":
            await _edit_html(
                query,
                f"<b>Tip of the day</b>\n\n{random.choice(TIPS)}",
                reply_markup=tools_keyboard(),
            )
        elif tool == "time":
            await _edit_html(
                query,
                f"<b>Server time (UTC)</b>\n\n{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
                reply_markup=tools_keyboard(),
            )
        elif tool == "calc":
            if len(parts) > 2:
                expr = parts[2]
                result = _safe_calc(expr)
                label = f"<b>Quick calc</b>\n\n<code>{expr}</code> = <b>{result}</b>"
            else:
                label = (
                    "<b>Custom calculator</b>\n\n"
                    "Send a message like: <code>calc 12 * 4 + 3</code>"
                )
            await _edit_html(query, label, reply_markup=tools_keyboard())
        elif tool == "health":
            llm = "ok" if settings.resolve_llm() else "missing API key"
            await _edit_html(
                query,
                confirmation_card("Bot Health", [f"Status: OK", f"LLM: {llm}"]),
                reply_markup=tools_keyboard(),
            )
        return None

    if data.startswith("settings:"):
        action = data.split(":", 1)[1]
        if action == "clear_ai":
            await db.clear_chat_history(user.id)
            await _edit_html(
                query,
                "<b>AI memory cleared</b>\n\nYour conversation history has been removed.",
                reply_markup=settings_keyboard(),
            )
        elif action == "stats":
            s = await db.stats()
            mode = await db.get_mode(user.id)
            await _edit_html(
                query,
                confirmation_card(
                    "Your Account",
                    [
                        f"User ID: {user.id}",
                        f"Current mode: {mode}",
                        f"Global users: {s['users']}",
                    ],
                ),
                reply_markup=settings_keyboard(),
            )
        return None

    return None


def _safe_calc(expr: str) -> str:
    if not re.match(r"^[\d\s+\-*/().]+$", expr):
        return "invalid expression"
    try:
        result = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 — sandboxed demo calc
        return str(result)
    except Exception:
        return "invalid expression"


async def book_date_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.effective_message or not update.effective_message.text:
        return BOOK_DATE
    text = update.effective_message.text.strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        await _reply_html(
            update.effective_message,
            f"{step_label(2, 3, 'Pick a date')}\n\nUse format <code>YYYY-MM-DD</code> (e.g. 2026-07-15)",
        )
        return BOOK_DATE
    context.user_data["book_date"] = text
    await _reply_html(
        update.effective_message,
        f"{step_label(3, 3, 'Pick a time')}\n\nSelect a slot:",
        reply_markup=booking_times_keyboard(),
    )
    return BOOK_TIME


async def ticket_desc_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.effective_message or not update.effective_message.text:
        return TICKET_DESC
    context.user_data["ticket_desc"] = update.effective_message.text.strip()[:2000]
    await _reply_html(
        update.effective_message,
        f"{step_label(3, 3, 'Set priority')}\n\nHow urgent is this?",
        reply_markup=support_priority_keyboard(),
    )
    return TICKET_PRI


async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message or not update.effective_message.text:
        return
    if not await _guard_rate(update):
        return

    user = update.effective_user
    text = update.effective_message.text.strip()
    await db.upsert_user(user.id, user.username, user.first_name)
    mode = await db.get_mode(user.id)

    lower = text.lower()
    if lower in ("main hub", "/menu", "menu"):
        await menu_cmd(update, context)
        return
    if lower in ("ask ai", "/ai", "ai"):
        await ai_cmd(update, context)
        return
    if lower in ("faq", "/faq"):
        await faq_cmd(update, context)
        return
    if lower in ("book", "/book"):
        await db.set_mode(user.id, "book")
        await _reply_html(
            update.effective_message,
            f"{step_label(1, 3, 'Select a service')}\n\nChoose the appointment type:",
            reply_markup=booking_services_keyboard(),
        )
        return
    if lower in ("support", "/support"):
        await db.set_mode(user.id, "support")
        await _reply_html(
            update.effective_message,
            f"{step_label(1, 3, 'Ticket category')}\n\nWhat area do you need help with?",
            reply_markup=support_category_keyboard(),
        )
        return

    if lower.startswith("calc "):
        expr = text[5:].strip()
        result = _safe_calc(expr)
        if result == "invalid expression":
            await _reply_html(update.effective_message, "Only numbers and + - * / ( ) allowed.")
        else:
            await _reply_html(update.effective_message, f"<b>Result</b>\n\n<code>{expr}</code> = <b>{result}</b>")
        return

    if mode == "ai" or lower.startswith("/ai"):
        await update.effective_message.chat.send_action("typing")
        history = await db.get_recent_messages(user.id)
        reply = await chat_completion(user.id, text, history)
        await db.add_message(user.id, "user", text)
        await db.add_message(user.id, "assistant", reply)
        await _track(user.id, "ai_message")
        await update.effective_message.reply_text(reply, parse_mode=PARSE_MODE)
        return

    if mode == "faq":
        hit = match_faq(text)
        if hit:
            await _reply_html(update.effective_message, faq_answer(hit["q"], hit["a"]))
        else:
            await _reply_html(
                update.effective_message,
                "No exact FAQ match. Browse categories below or switch to <b>Ask AI</b>.",
                reply_markup=faq_categories_keyboard(),
            )
        return

    hit = match_faq(text)
    if hit:
        await _reply_html(update.effective_message, faq_answer(hit["q"], hit["a"]))
        return

    await _reply_html(
        update.effective_message,
        "I didn't catch that. Open the <b>Main Hub</b> or try Ask AI, FAQ, Book, or Support.",
        reply_markup=main_menu_keyboard(),
    )


def build_application() -> Application:
    app = Application.builder().token(settings.telegram_bot_token).build()

    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback_router, pattern="^mode:"),
            CallbackQueryHandler(callback_router, pattern="^booksvc:"),
            CallbackQueryHandler(callback_router, pattern="^ticketcat:"),
        ],
        states={
            BOOK_SERVICE: [CallbackQueryHandler(callback_router)],
            BOOK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, book_date_text)],
            BOOK_TIME: [CallbackQueryHandler(callback_router)],
            TICKET_CAT: [CallbackQueryHandler(callback_router)],
            TICKET_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, ticket_desc_text)],
            TICKET_PRI: [CallbackQueryHandler(callback_router)],
        },
        fallbacks=[
            CommandHandler("menu", menu_cmd),
            CallbackQueryHandler(callback_router, pattern="^(menu|nav:menu)$"),
        ],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("forget", forget_cmd))
    app.add_handler(CommandHandler("review", review_cmd))
    app.add_handler(CommandHandler("health", health_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("ai", ai_cmd))
    app.add_handler(CommandHandler("faq", faq_cmd))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

    return app
