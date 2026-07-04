from __future__ import annotations

import logging

from openai import AsyncOpenAI

from bot.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Tendem Assistant by Zachary Hutton, a professional messaging bot for a hybrid AI + human support platform.

Persona:
- Warm, confident, and concise — like a skilled front-desk agent, not a generic chatbot.
- You represent Tendem: hybrid AI with human escalation for complex issues.

You help with appointments, product questions, troubleshooting, and general guidance.

Rules:
- Keep replies concise (2-4 sentences unless the user asks for detail).
- Use friendly, professional tone. No em dashes.
- If you do not know something, say so and offer to open a support ticket via /support.
- Never invent prices, policies, or account details.
- Suggest /menu to return to the Main Hub when stuck.
- You may use simple formatting sparingly (e.g. bullet points) but avoid markdown headers.
"""


async def chat_completion(user_id: int, user_message: str, history: list[dict[str, str]]) -> str:
    resolved = settings.resolve_llm()
    if not resolved:
        return (
            "AI chat is not configured on this demo instance. "
            "Try FAQ mode from /menu or open a support ticket. "
            "(Set GROQ_API_KEY or OPENAI_API_KEY to enable LLM responses.)"
        )

    provider, api_key, model = resolved
    client_kwargs: dict = {"api_key": api_key}
    if provider == "groq":
        client_kwargs["base_url"] = "https://api.groq.com/openai/v1"

    client = AsyncOpenAI(**client_kwargs)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=400,
        )
        text = (response.choices[0].message.content or "").strip()
        return text or "I could not generate a response. Please try again or use /menu."
    except Exception as exc:
        logger.exception("LLM request failed for user %s: %s", user_id, exc)
        return (
            "Sorry, the AI service is temporarily unavailable. "
            "Your message was not lost. Try again in a moment or use Support from /menu."
        )
