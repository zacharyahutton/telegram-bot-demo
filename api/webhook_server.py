"""Webhook mode — FastAPI + Telegram webhook (production-style)."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Request
from telegram import Update

from bot.config import settings
from bot.database import db
from bot.handlers.core import build_application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ptb_app = build_application()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await db.connect()
    await ptb_app.initialize()
    await ptb_app.start()
    if settings.webhook_url:
        webhook_url = f"{settings.webhook_url.rstrip('/')}/telegram/webhook"
        await ptb_app.bot.set_webhook(
            url=webhook_url,
            secret_token=settings.webhook_secret or None,
            drop_pending_updates=True,
        )
        logger.info("Webhook registered: %s", webhook_url)
    yield
    await ptb_app.stop()
    await ptb_app.shutdown()
    await db.close()


app = FastAPI(title="Tendem Demo Bot Webhook", lifespan=lifespan)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "llm": bool(settings.resolve_llm()),
        "webhook_configured": bool(settings.webhook_url),
    }


@app.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if settings.webhook_secret and x_telegram_bot_api_secret_token != settings.webhook_secret:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)
    await ptb_app.process_update(update)
    return {"ok": True}
