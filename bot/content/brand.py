"""Tendem brand copy and Telegram HTML formatting helpers."""

from __future__ import annotations

BRAND_NAME = "Tendem"
BRAND_FULL = "Tendem by Zachary Hutton"
TAGLINE = "Hybrid AI + human messaging"
DIVIDER = "━━━━━━━━━━━━━━━━━━━━"
PARSE_MODE = "HTML"

WELCOME_TEXT = (
    f"<b>{BRAND_NAME}</b>\n"
    f"<i>{TAGLINE}</i>\n\n"
    "Welcome. I handle appointments, support tickets, and product questions — "
    "with AI assistance and human escalation when it matters.\n\n"
    f"{DIVIDER}\n"
    "<b>Get started</b>\n"
    "Tap a button below or open the Main Hub.\n\n"
    "Hiring reviewer? Send /review for a 60-second capability tour."
)

MAIN_MENU_TEXT = (
    f"<b>Main Hub</b>\n"
    f"{DIVIDER}\n\n"
    "<b>Conversations</b>\n"
    "AI Chat · FAQ knowledge base\n\n"
    "<b>Services</b>\n"
    "Book appointment · Open support ticket\n\n"
    "<b>More</b>\n"
    "Tools · Settings · About\n\n"
    "<i>Quick actions are pinned below.</i>"
)

ABOUT_TEXT = (
    f"<b>About {BRAND_FULL}</b>\n"
    f"{DIVIDER}\n\n"
    "Built for Mindrift / Tendem-style messaging work: hybrid AI plus structured "
    "workflows on Telegram, with patterns that transfer to WhatsApp and Discord.\n\n"
    "<b>What this demo proves</b>\n"
    "• Multi-step booking and support flows with progress tracking\n"
    "• LLM chat with SQLite memory and FAQ fallbacks\n"
    "• Webhook-ready FastAPI backend for 24/7 deployment\n"
    "• Rate limiting, admin analytics, and user data controls\n\n"
    "<b>Built by</b> Zachary Hutton · Portmore, Jamaica\n"
    "<b>Portfolio</b> zachary-hutton-portfolio.vercel.app\n"
    "<b>Source</b> github.com/zacharyahutton/telegram-bot-demo"
)

REVIEWER_TOUR_TEXT = (
    f"<b>{BRAND_NAME} — Reviewer Tour</b>\n"
    f"<i>60 seconds · built for Tendem hiring</i>\n"
    f"{DIVIDER}\n\n"
    "<b>1 · Conversational flows</b>\n"
    "/book — service → date → time → confirmation card\n"
    "/support — category → description → priority → ticket ID\n\n"
    "<b>2 · LLM + fallbacks</b>\n"
    "/ai — Groq/OpenAI with SQLite memory\n"
    "/faq — 30+ curated answers across 8 categories\n\n"
    "<b>3 · Production patterns</b>\n"
    "/health — liveness + LLM status\n"
    "Rate limiting on spam · /forget for data deletion\n\n"
    "<b>4 · Webhook backend</b>\n"
    "GET /health · POST /telegram/webhook with secret-token validation\n\n"
    "<b>5 · Admin</b> (set ADMIN_USER_IDS)\n"
    "/stats — users, bookings, tickets, events\n\n"
    "<b>6 · Cross-platform</b>\n"
    "Search FAQ for \"whatsapp\" or \"discord\"\n\n"
    f"{DIVIDER}\n"
    "<b>Try now:</b> /book → /support → /ai"
)

AI_MODE_TEXT = (
    f"<b>{BRAND_NAME} Assistant</b>\n"
    f"{DIVIDER}\n\n"
    "I'm your AI guide for product questions, troubleshooting, and general help. "
    "I remember recent messages in this session.\n\n"
    "Send a message to begin. Use /menu to return to the Main Hub."
)

FAQ_MODE_TEXT = (
    f"<b>Knowledge Base</b>\n"
    f"{DIVIDER}\n\n"
    "Browse by category or type a question — I'll match keywords from 30+ curated answers."
)

TOOLS_MODE_TEXT = (
    f"<b>Tools</b>\n"
    f"{DIVIDER}\n\n"
    "Quick utilities for demos and day-to-day checks. Pick one below."
)

SETTINGS_MODE_TEXT = (
    f"<b>Settings</b>\n"
    f"{DIVIDER}\n\n"
    "Manage your session preferences and view account info."
)

HELP_TEXT = (
    f"<b>{BRAND_NAME} Commands</b>\n"
    f"{DIVIDER}\n\n"
    "/start — Welcome + Main Hub\n"
    "/menu — Return to Main Hub\n"
    "/about — Brand story and architecture\n"
    "/review — 60-sec tour for hiring reviewers\n"
    "/ai — AI assistant mode\n"
    "/faq — Knowledge base categories\n"
    "/book — Appointment booking\n"
    "/support — Support ticket\n"
    "/tools — Utilities\n"
    "/settings — Preferences\n"
    "/forget — Clear AI chat memory\n"
    "/health — Bot health check\n"
    "/stats — Admin analytics\n\n"
    "<i>Reply keyboard shortcuts: Main Hub, Ask AI, Book, Support</i>"
)


def step_label(current: int, total: int, title: str) -> str:
    return f"<b>Step {current} of {total}</b> · {title}"


def confirmation_card(title: str, lines: list[str], footer: str = "") -> str:
    body = "\n".join(f"• {line}" for line in lines)
    text = f"<b>{title}</b>\n{DIVIDER}\n\n{body}"
    if footer:
        text += f"\n\n{footer}"
    return text


def faq_answer(question: str, answer: str) -> str:
    return f"<b>Q:</b> {question}\n\n<b>A:</b> {answer}"
