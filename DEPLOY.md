# Run the bot 24/7 (Railway — ~10 minutes)

Your laptop off, bot still live. This uses **webhook mode** (Telegram pushes messages to your server).

## What you need

- GitHub repo with `telegram-bot-demo` (push the folder as its own repo)
- [Railway](https://railway.app) account (free tier works for demos)
- Bot token from [@BotFather](https://t.me/BotFather)
- Optional: `GROQ_API_KEY` for `/ai`

---

## Step 1 — Push code to GitHub

```powershell
cd C:\Users\EverybodyHatesA1one\Documents\telegram-bot-demo
git init
git add .
git commit -m "Tendem Demo Bot — webhook-ready Telegram bot"
git remote add origin https://github.com/zacharyahutton/telegram-bot-demo.git
git push -u origin main
```

(Create the empty repo on GitHub first if it does not exist.)

---

## Step 2 — Create Railway project

1. [railway.app/new](https://railway.app/new) → **Deploy from GitHub repo**
2. Select `telegram-bot-demo`
3. Railway auto-detects Python via `railway.toml`

---

## Step 3 — Set environment variables

In Railway → your service → **Variables**:

| Variable | Value |
|----------|--------|
| `TELEGRAM_BOT_TOKEN` | From BotFather |
| `GROQ_API_KEY` | From console.groq.com (optional) |
| `WEBHOOK_SECRET` | Random string, e.g. `openssl rand -hex 32` or any long password |
| `ADMIN_USER_IDS` | Your Telegram user ID ([@userinfobot](https://t.me/userinfobot)) |
| `DATABASE_PATH` | `/app/data/tendem_demo.db` |
| `PORT` | Railway sets this automatically — do not override |

**Do not set `WEBHOOK_URL` yet** — you need the public URL first.

---

## Step 4 — Deploy and get your URL

1. Railway deploys → **Settings** → **Networking** → **Generate domain**
2. Copy the URL, e.g. `https://telegram-bot-demo-production.up.railway.app`

---

## Step 5 — Register webhook

Add one more variable:

```
WEBHOOK_URL=https://YOUR-RAILWAY-DOMAIN.up.railway.app
```

(No trailing slash. The bot registers `…/telegram/webhook` on startup.)

Redeploy (or wait for auto-redeploy). Check logs for:

```
Webhook registered: https://…/telegram/webhook
```

---

## Step 6 — Verify

1. Open `https://YOUR-DOMAIN.up.railway.app/health` in a browser → `{"status":"ok",…}`
2. Open Telegram → your bot → `/start`
3. Send `/review` — 60-second capability tour
4. Test `/book`, `/support`, `/ai`, `/faq`

---

## Optional — persist SQLite on Railway

Railway disks reset on redeploy unless you attach a volume:

1. Service → **Volumes** → Add mount at `/app/data`
2. Keep `DATABASE_PATH=/app/data/tendem_demo.db`

For a demo deployment, ephemeral SQLite is usually fine.

---

## Local vs production

| Mode | Command | When |
|------|---------|------|
| Local dev | `start-bot.bat` or `python run_polling.py` | Building/testing on your PC |
| Production | `python run_webhook.py` (Railway start command) | 24/7 live demo |

**Important:** Stop local polling before going webhook-only, or Telegram may deliver to both.

To clear webhook and go back to polling locally:

```powershell
# In Python with your token loaded
# await bot.delete_webhook(drop_pending_updates=True)
```

Or use BotFather → `/deletebot` is nuclear; prefer deleting webhook via API or redeploy polling only when testing.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bot silent after deploy | Check Railway logs; confirm `WEBHOOK_URL` matches generated domain |
| 403 on webhook | `WEBHOOK_SECRET` must match what Telegram sends |
| `/ai` fails | Add `GROQ_API_KEY` or `OPENAI_API_KEY` |
| Health OK but no replies | Token wrong or webhook not registered — check logs on startup |

---

## Share your live demo

After deploy, your public links:

```
Live demo: t.me/YourBotUsername
Source: github.com/zacharyahutton/telegram-bot-demo
Health: https://YOUR-DOMAIN.up.railway.app/health
```

New users can send `/review` for a guided tour of all capabilities.
