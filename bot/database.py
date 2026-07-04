from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import aiosqlite

from bot.config import settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    mode TEXT DEFAULT 'menu',
    created_at REAL,
    updated_at REAL
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT NOT NULL,
    payload TEXT,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS rate_limits (
    user_id INTEGER PRIMARY KEY,
    window_start REAL NOT NULL,
    count INTEGER NOT NULL
);
"""


class Database:
    def __init__(self, path: str | None = None) -> None:
        self.path = path or settings.database_path
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.executescript(_SCHEMA)
        await self._conn.commit()

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None

    @property
    def conn(self) -> aiosqlite.Connection:
        if not self._conn:
            raise RuntimeError("Database not connected")
        return self._conn

    async def upsert_user(self, user_id: int, username: str | None, first_name: str | None) -> None:
        now = time.time()
        await self.conn.execute(
            """
            INSERT INTO users (user_id, username, first_name, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                updated_at=excluded.updated_at
            """,
            (user_id, username, first_name, now, now),
        )
        await self.conn.commit()

    async def set_mode(self, user_id: int, mode: str) -> None:
        await self.conn.execute(
            "UPDATE users SET mode=?, updated_at=? WHERE user_id=?",
            (mode, time.time(), user_id),
        )
        await self.conn.commit()

    async def get_mode(self, user_id: int) -> str:
        cur = await self.conn.execute("SELECT mode FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row["mode"] if row else "menu"

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        await self.conn.execute(
            "INSERT INTO chat_history (user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, content, time.time()),
        )
        await self.conn.commit()

    async def get_recent_messages(self, user_id: int, limit: int = 12) -> list[dict[str, str]]:
        cur = await self.conn.execute(
            """
            SELECT role, content FROM chat_history
            WHERE user_id=? ORDER BY id DESC LIMIT ?
            """,
            (user_id, limit),
        )
        rows = await cur.fetchall()
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    async def clear_chat_history(self, user_id: int) -> None:
        await self.conn.execute("DELETE FROM chat_history WHERE user_id=?", (user_id,))
        await self.conn.commit()

    async def create_booking(
        self, user_id: int, service: str, booking_date: str, booking_time: str
    ) -> int:
        cur = await self.conn.execute(
            """
            INSERT INTO bookings (user_id, service, booking_date, booking_time, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, service, booking_date, booking_time, time.time()),
        )
        await self.conn.commit()
        return cur.lastrowid or 0

    async def create_ticket(
        self, user_id: int, category: str, description: str, priority: str
    ) -> int:
        cur = await self.conn.execute(
            """
            INSERT INTO support_tickets (user_id, category, description, priority, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, category, description, priority, time.time()),
        )
        await self.conn.commit()
        return cur.lastrowid or 0

    async def log_event(self, user_id: int | None, event_type: str, payload: Any = None) -> None:
        await self.conn.execute(
            "INSERT INTO analytics_events (user_id, event_type, payload, created_at) VALUES (?, ?, ?, ?)",
            (user_id, event_type, json.dumps(payload) if payload is not None else None, time.time()),
        )
        await self.conn.commit()

    async def stats(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for table, key in [
            ("users", "users"),
            ("bookings", "bookings"),
            ("support_tickets", "tickets"),
            ("analytics_events", "events"),
        ]:
            cur = await self.conn.execute(f"SELECT COUNT(*) AS c FROM {table}")
            row = await cur.fetchone()
            out[key] = int(row["c"]) if row else 0
        return out

    async def check_rate_limit(self, user_id: int, max_per_minute: int = 20) -> bool:
        now = time.time()
        window = 60.0
        cur = await self.conn.execute(
            "SELECT window_start, count FROM rate_limits WHERE user_id=?", (user_id,)
        )
        row = await cur.fetchone()
        if not row or now - row["window_start"] > window:
            await self.conn.execute(
                """
                INSERT INTO rate_limits (user_id, window_start, count) VALUES (?, ?, 1)
                ON CONFLICT(user_id) DO UPDATE SET window_start=?, count=1
                """,
                (user_id, now, now),
            )
            await self.conn.commit()
            return True
        if row["count"] >= max_per_minute:
            return False
        await self.conn.execute(
            "UPDATE rate_limits SET count=count+1 WHERE user_id=?", (user_id,)
        )
        await self.conn.commit()
        return True


db = Database()
