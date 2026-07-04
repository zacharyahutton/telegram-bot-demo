from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from bot.content.brand import (
    ABOUT_TEXT,
    AI_MODE_TEXT,
    FAQ_MODE_TEXT,
    MAIN_MENU_TEXT,
    REVIEWER_TOUR_TEXT,
    SETTINGS_MODE_TEXT,
    TOOLS_MODE_TEXT,
    WELCOME_TEXT,
)

# Re-export for handlers that import from here
__all__ = [
    "ABOUT_TEXT",
    "AI_MODE_TEXT",
    "FAQ_MODE_TEXT",
    "MAIN_MENU_TEXT",
    "REVIEWER_TOUR_TEXT",
    "SETTINGS_MODE_TEXT",
    "TOOLS_MODE_TEXT",
    "WELCOME_TEXT",
    "about_keyboard",
    "booking_services_keyboard",
    "booking_times_keyboard",
    "faq_categories_keyboard",
    "faq_category_items_keyboard",
    "main_menu_keyboard",
    "persistent_reply_keyboard",
    "quick_actions_row",
    "settings_keyboard",
    "support_category_keyboard",
    "support_priority_keyboard",
    "tools_keyboard",
]


def quick_actions_row() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton("Ask AI", callback_data="mode:ai"),
        InlineKeyboardButton("FAQ", callback_data="mode:faq"),
        InlineKeyboardButton("Book", callback_data="mode:book"),
    ]


def _back_row(label: str = "← Main Hub") -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(label, callback_data="nav:menu")]


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        quick_actions_row(),
        [
            InlineKeyboardButton("AI Chat", callback_data="mode:ai"),
            InlineKeyboardButton("Knowledge Base", callback_data="mode:faq"),
        ],
        [
            InlineKeyboardButton("Book Appointment", callback_data="mode:book"),
            InlineKeyboardButton("Support Ticket", callback_data="mode:support"),
        ],
        [
            InlineKeyboardButton("Tools", callback_data="mode:tools"),
            InlineKeyboardButton("Settings", callback_data="mode:settings"),
        ],
        [
            InlineKeyboardButton("About Tendem", callback_data="mode:about"),
            InlineKeyboardButton("Capability Tour", callback_data="mode:review"),
        ],
    ])


def about_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Start Capability Tour", callback_data="mode:review")],
        _back_row(),
    ])


def faq_categories_keyboard() -> InlineKeyboardMarkup:
    from bot.content.faq import FAQ_CATEGORIES

    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for key, label in FAQ_CATEGORIES.items():
        row.append(InlineKeyboardButton(label, callback_data=f"faqcat:{key}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append(_back_row())
    return InlineKeyboardMarkup(rows)


def faq_category_items_keyboard(category: str) -> InlineKeyboardMarkup:
    from bot.content.faq import FAQ_ENTRIES, list_faq_by_category

    items = list_faq_by_category(category)[:8]
    rows: list[list[InlineKeyboardButton]] = []
    for entry in items:
        try:
            idx = FAQ_ENTRIES.index(entry)
        except ValueError:
            continue
        label = entry["q"][:38] + ("…" if len(entry["q"]) > 38 else "")
        rows.append([InlineKeyboardButton(label, callback_data=f"faqidx:{idx}")])
    rows.append([InlineKeyboardButton("← All categories", callback_data="mode:faq")])
    rows.append(_back_row())
    return InlineKeyboardMarkup(rows)


def booking_services_keyboard() -> InlineKeyboardMarkup:
    services = ["Consultation", "Demo walkthrough", "Technical review", "Onboarding call"]
    rows = [[InlineKeyboardButton(s, callback_data=f"booksvc:{s}")] for s in services]
    rows.append(_back_row("← Cancel"))
    return InlineKeyboardMarkup(rows)


def booking_times_keyboard() -> InlineKeyboardMarkup:
    times = ["09:00", "11:00", "14:00", "16:00", "18:00"]
    rows = [[InlineKeyboardButton(t, callback_data=f"booktime:{t}")] for t in times]
    rows.append(_back_row("← Cancel"))
    return InlineKeyboardMarkup(rows)


def support_category_keyboard() -> InlineKeyboardMarkup:
    cats = ["Billing", "Technical", "Account", "Integration", "Other"]
    rows = [[InlineKeyboardButton(c, callback_data=f"ticketcat:{c}")] for c in cats]
    rows.append(_back_row("← Cancel"))
    return InlineKeyboardMarkup(rows)


def support_priority_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Low", callback_data="ticketpri:low"),
            InlineKeyboardButton("Normal", callback_data="ticketpri:normal"),
            InlineKeyboardButton("Urgent", callback_data="ticketpri:urgent"),
        ],
        _back_row("← Cancel"),
    ])


def tools_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Tip of the day", callback_data="tool:tip"),
            InlineKeyboardButton("Server time (UTC)", callback_data="tool:time"),
        ],
        [
            InlineKeyboardButton("Quick calc: 12×4", callback_data="tool:calc:12*4"),
            InlineKeyboardButton("Quick calc: 15% of 200", callback_data="tool:calc:200*0.15"),
        ],
        [
            InlineKeyboardButton("Custom calc", callback_data="tool:calc"),
            InlineKeyboardButton("Bot health", callback_data="tool:health"),
        ],
        _back_row(),
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Clear AI memory", callback_data="settings:clear_ai")],
        [InlineKeyboardButton("My account info", callback_data="settings:stats")],
        _back_row(),
    ])


def persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Main Hub"), KeyboardButton("Ask AI")],
            [KeyboardButton("Book"), KeyboardButton("Support")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Message Tendem…",
    )
