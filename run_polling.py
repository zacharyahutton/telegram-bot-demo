"""Polling mode — local development."""

from __future__ import annotations

import asyncio
import logging

from bot.database import db
from bot.handlers.core import build_application

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await db.connect()
    app = build_application()
    logger.info("Starting Tendem Demo Bot in polling mode...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
