# Tendem by Zachary Hutton

Production-style **Telegram bot** built as a portfolio piece for Mindrift / Tendem (AI Pilot — Bot Developer) applications.

**Tendem** is a branded hybrid messaging experience: structured workflows (booking, support tickets, FAQ) plus an AI assistant with human escalation — not a generic demo bot.

Demonstrates messaging-platform patterns that transfer to **WhatsApp Business API**, **Telegram Bot API**, and **Discord**:

- Branded Main Hub with quick actions, category navigation, and persistent reply keyboard
- Multi-step flows with step progress indicators and confirmation cards
- LLM integration (Groq / OpenAI) with Tendem assistant persona and memory
- 30+ FAQ entries with rich category intros
- Inline keyboards with back navigation (`nav:menu`), edit-in-place UX
- SQLite persistence (users, chat history, bookings, tickets, analytics)
- Per-user rate limiting
- Admin commands (`/stats`, `/health`)
- **Webhook mode** (FastAPI + secret token validation)
- **Polling mode** for local dev

## Quick start

```bash
cd telegram-bot-demo
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env
```

1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram
2. Paste `TELEGRAM_BOT_TOKEN` into `.env`
3. Optional: set `GROQ_API_KEY` or `OPENAI_API_KEY` for AI chat
4. Optional: set `ADMIN_USER_IDS` to your Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot))

### Local (polling)

```bash
python run_polling.py
```

Open your bot in Telegram and send `/start`.

### Production (webhook — runs 24/7)

See **[DEPLOY.md](./DEPLOY.md)** for the full Railway guide.

```bash
# Set WEBHOOK_URL=https://your-app.up.railway.app in .env
python run_webhook.py
```

Endpoints:

- `GET /health` — liveness
- `POST /telegram/webhook` — Telegram updates (validates `X-Telegram-Bot-Api-Secret-Token`)

**Hiring reviewers:** send `/review` for a 60-second capability tour, or `/about` for the brand story.

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Branded welcome + Main Hub |
| `/menu` | Main Hub |
| `/about` | Brand story and architecture |
| `/ai` | Tendem AI assistant mode |
| `/faq` | Knowledge base (30+ topics) |
| `/book` | Appointment booking flow |
| `/support` | Support ticket flow |
| `/tools` | Tips, time, quick calc, health |
| `/settings` | Clear AI memory, account info |
| `/forget` | Clear chat history |
| `/review` | 60-sec tour for Mindrift/Tendem reviewers |
| `/health` | Bot health check |
| `/stats` | Admin analytics |

## Architecture

```
telegram-bot-demo/
  bot/
    handlers/core.py    # Commands, callbacks, conversation flows
    content/brand.py    # Tendem brand copy and HTML helpers
    content/faq.py      # FAQ knowledge base
    keyboards/menus.py  # Inline / reply keyboards
    services/llm.py     # Groq / OpenAI chat
    database.py         # SQLite (aiosqlite)
    config.py           # pydantic-settings
  api/webhook_server.py # FastAPI webhook receiver
  run_polling.py
  run_webhook.py
```

## Deploy (Railway / Render)

1. Set env vars from `.env.example`
2. Start command: `python run_webhook.py`
3. Set `WEBHOOK_URL` to your public HTTPS URL
4. Register webhook automatically on startup

## Author

**Zachary Hutton** — Portmore, Jamaica  
Portfolio: https://zachary-hutton-portfolio.vercel.app/  
GitHub: https://github.com/zacharyahutton/telegram-bot-demo

Built for Mindrift Tendem freelance Bot Developer (AI Pilot) applications.
