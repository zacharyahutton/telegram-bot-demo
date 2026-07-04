"""FAQ knowledge base — keyword routing with 40+ curated responses."""

from __future__ import annotations

FAQ_CATEGORIES = {
    "getting_started": "Getting started",
    "booking": "Booking & appointments",
    "billing": "Billing & payments",
    "technical": "Technical support",
    "integrations": "Integrations & APIs",
    "ai": "AI & automation",
    "privacy": "Privacy & security",
    "account": "Account & profile",
}

FAQ_ENTRIES: list[dict] = [
    {"keys": ["start", "hello", "hi", "hey"], "cat": "getting_started", "q": "How do I start?", "a": "Send /start or /menu. Pick AI Chat, FAQ, Book Appointment, or Open Support Ticket."},
    {"keys": ["menu", "main menu", "options"], "cat": "getting_started", "q": "Main menu", "a": "Use /menu anytime to see all features: AI assistant, FAQ, booking flow, support tickets, tools, and settings."},
    {"keys": ["hours", "open", "availability"], "cat": "getting_started", "q": "Business hours", "a": "This demo bot is available 24/7. Human agents on Tendem typically respond within business hours (configurable per deployment)."},
    {"keys": ["language", "english", "spanish"], "cat": "getting_started", "q": "Languages", "a": "This demo runs in English. Production Tendem bots can be localized per channel and region."},
    {"keys": ["human", "agent", "person"], "cat": "getting_started", "q": "Talk to a human", "a": "Open a Support Ticket from /menu. Choose priority and describe your issue. A human agent can pick it up in the Tendem hybrid workflow."},
    {"keys": ["book", "appointment", "schedule", "meeting"], "cat": "booking", "q": "Book appointment", "a": "Tap Book Appointment in /menu. Select service, date, and time. You will get a confirmation with a booking ID."},
    {"keys": ["reschedule", "change appointment"], "cat": "booking", "q": "Reschedule", "a": "For this demo, create a new booking and note the old ID in a support ticket. Production bots can link to calendar APIs."},
    {"keys": ["cancel appointment", "cancel booking"], "cat": "booking", "q": "Cancel booking", "a": "Reply with your booking ID in a support ticket, or use /mybookings if enabled in your deployment."},
    {"keys": ["reminder", "notification"], "cat": "booking", "q": "Reminders", "a": "Production deployments send template-based reminders via WhatsApp/Telegram before appointments."},
    {"keys": ["price", "cost", "fee", "payment"], "cat": "billing", "q": "Pricing", "a": "This is a demo bot. In production, pricing is configured per business and can be shown via secure payment links."},
    {"keys": ["invoice", "receipt"], "cat": "billing", "q": "Invoices", "a": "Request an invoice through Support with your account email. Integrations can attach PDF receipts automatically."},
    {"keys": ["refund"], "cat": "billing", "q": "Refunds", "a": "Refund policies are set per business. Open a billing support ticket and a human agent will review."},
    {"keys": ["card", "stripe", "pay"], "cat": "billing", "q": "Payments", "a": "Payment bots typically use secure checkout links (Stripe, etc.) sent as interactive messages, not raw card collection in chat."},
    {"keys": ["slow", "lag", "not responding"], "cat": "technical", "q": "Bot slow", "a": "Check your connection. If AI mode fails, we log the error server-side. Try /menu and FAQ, or open a support ticket."},
    {"keys": ["error", "broken", "bug"], "cat": "technical", "q": "Something broke", "a": "Use /health to check bot status. Describe what you tapped before the error in a support ticket for fastest help."},
    {"keys": ["webhook"], "cat": "technical", "q": "Webhooks", "a": "This bot supports webhook mode via FastAPI with secret token validation, ideal for production on Railway, Render, or VPS."},
    {"keys": ["rate limit", "too many"], "cat": "technical", "q": "Rate limits", "a": "Users are rate-limited per minute to prevent abuse. Platform APIs (WhatsApp, Telegram) have their own limits too."},
    {"keys": ["whatsapp", "telegram", "discord"], "cat": "integrations", "q": "Platforms", "a": "Tendem targets WhatsApp Business API, Telegram Bot API, and Discord. This demo implements Telegram with patterns that transfer across platforms."},
    {"keys": ["api", "rest", "integrate"], "cat": "integrations", "q": "APIs", "a": "Bots connect to CRMs, booking systems, and databases via REST webhooks. State is stored in SQLite here; MongoDB/Postgres in production."},
    {"keys": ["crm", "hubspot", "salesforce"], "cat": "integrations", "q": "CRM", "a": "Lead and ticket data can sync to CRM via outbound webhooks when a conversation completes or escalates."},
    {"keys": ["llm", "gpt", "openai", "groq", "anthropic", "ai"], "cat": "ai", "q": "AI features", "a": "AI Chat uses Groq or OpenAI with conversation memory, fallbacks, and guardrails. Human agents can override in Tendem hybrid mode."},
    {"keys": ["prompt", "hallucination", "wrong answer"], "cat": "ai", "q": "AI accuracy", "a": "We use system prompts, FAQ fallbacks, and human escalation. Never trust AI for account-specific facts without verification."},
    {"keys": ["template", "whatsapp template"], "cat": "ai", "q": "Templates", "a": "WhatsApp requires approved templates for outbound messages outside the 24h window. Telegram/Discord are more flexible for proactive messages."},
    {"keys": ["privacy", "data", "gdpr"], "cat": "privacy", "q": "Privacy", "a": "Conversation data is stored for demo purposes. Production deployments should define retention, export, and deletion policies."},
    {"keys": ["delete", "erase", "forget"], "cat": "privacy", "q": "Delete my data", "a": "Send /forget to clear your chat history in this demo. Production bots should implement full data deletion workflows."},
    {"keys": ["secure", "encryption", "ssl"], "cat": "privacy", "q": "Security", "a": "Use HTTPS webhooks, validate Telegram secret tokens, sign outbound webhooks with HMAC, and never log secrets."},
    {"keys": ["password", "login", "account"], "cat": "account", "q": "Account access", "a": "This demo does not manage passwords. Link Telegram user ID to your account in production via OTP or magic link."},
    {"keys": ["profile", "name", "update"], "cat": "account", "q": "Update profile", "a": "Telegram provides your display name automatically. Business-specific profile fields sync from your CRM."},
    {"keys": ["block", "spam", "report"], "cat": "account", "q": "Report abuse", "a": "Admins can use moderation commands. Users who spam are rate-limited automatically."},
    {"keys": ["demo", "portfolio", "tendem", "about"], "cat": "getting_started", "q": "About this bot", "a": "Tendem Demo Bot by Zachary Hutton — a portfolio project showcasing conversational flows, LLM integration, webhooks, SQLite state, booking, tickets, FAQ, and admin tools for hybrid AI messaging."},
    {"keys": ["features", "what can you do"], "cat": "getting_started", "q": "Features", "a": "AI chat, 30+ FAQ topics, appointment booking, support tickets, utilities (time, calc, tips), admin stats, rate limiting, webhook mode, and persistent conversation memory."},
    {"keys": ["github", "source", "code"], "cat": "getting_started", "q": "Source code", "a": "Open source at github.com/zacharyahutton/telegram-bot-demo. Python, python-telegram-bot, FastAPI, SQLite."},
    {"keys": ["help", "support", "assist"], "cat": "technical", "q": "Help", "a": "Type /menu for options, /faq for topics, or open a Support Ticket. Admins: /stats /health."},
]

CATEGORY_INTROS = {
    "getting_started": (
        "<b>Getting Started</b>\n"
        "Navigation, business hours, languages, and how to reach a human agent."
    ),
    "booking": (
        "<b>Booking & Appointments</b>\n"
        "Schedule, reschedule, cancel, and reminder policies."
    ),
    "billing": (
        "<b>Billing & Payments</b>\n"
        "Pricing, invoices, refunds, and secure payment links."
    ),
    "technical": (
        "<b>Technical Support</b>\n"
        "Errors, performance, webhooks, and rate limits."
    ),
    "integrations": (
        "<b>Integrations & APIs</b>\n"
        "WhatsApp, Telegram, Discord, CRM sync, and REST webhooks."
    ),
    "ai": (
        "<b>AI & Automation</b>\n"
        "LLMs, prompt guardrails, templates, and hybrid human handoff."
    ),
    "privacy": (
        "<b>Privacy & Security</b>\n"
        "Data retention, deletion, encryption, and compliance."
    ),
    "account": (
        "<b>Account & Profile</b>\n"
        "Login, profile updates, and abuse reporting."
    ),
}


def match_faq(text: str) -> dict | None:
    lower = text.lower().strip()
    for entry in FAQ_ENTRIES:
        if any(k in lower for k in entry["keys"]):
            return entry
    return None


def list_faq_by_category(category: str) -> list[dict]:
    return [e for e in FAQ_ENTRIES if e["cat"] == category]
