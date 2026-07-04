# Tendem Demo Bot

**Hybrid AI + human messaging on Telegram**

[Open in Telegram](https://t.me/zachtedembot) | Search for **Tendem Demo Bot** or use your deployment link

---

## What it is

**Tendem Demo Bot** is a portfolio Telegram assistant built by Zachary Hutton. It shows how a business messaging bot can combine structured workflows (booking, support, FAQ) with an AI assistant that remembers your conversation — and escalates to human-style flows when needed.

Send `/start` to open the **Main Hub**: a branded home screen with quick actions, category navigation, and a persistent reply keyboard for one-tap access.

---

## Features

- **Main Hub** — Branded welcome, inline menus, and pinned shortcuts (Main Hub, Ask AI, Book, Support)
- **AI assistant** — Chat with the Tendem assistant; session memory stored per user (`/ai` or **Ask AI**)
- **Knowledge base** — 30+ curated FAQ answers across 8 categories; browse by topic or type a question for keyword matching (`/faq`)
- **Appointment booking** — 3-step flow: service → date → time slot → confirmation card (`/book`)
- **Support tickets** — 3-step flow: category → description → priority → ticket ID (`/support`)
- **Tools** — Tip of the day, UTC server time, quick calculator, bot health check
- **Settings** — Clear AI memory, view account info (`/settings`, `/forget`)
- **Reviewer tour** — 60-second capability walkthrough for hiring reviewers (`/review`)
- **Privacy controls** — `/forget` removes your AI chat history from this demo instance

---

## Commands

| Command | What it does |
|---------|--------------|
| `/start` | Welcome message + Main Hub |
| `/menu` | Return to Main Hub |
| `/about` | Brand story and what this demo proves |
| `/review` | 60-second tour for hiring reviewers |
| `/ai` | Enter AI assistant mode |
| `/faq` | Browse the knowledge base |
| `/book` | Start appointment booking |
| `/support` | Open a support ticket |
| `/tools` | Utilities (tips, time, calculator, health) |
| `/settings` | Preferences and account info |
| `/forget` | Clear your AI chat memory |
| `/health` | Bot health check |

**Reply keyboard shortcuts:** Main Hub, Ask AI, Book, Support

---

## Quick walkthrough (reviewers)

1. **`/start`** — See the branded welcome and Main Hub with inline buttons and reply keyboard.
2. **`/review`** — Read the guided 60-second tour of all capabilities.
3. **`/book`** — Pick a service (Consultation, Demo walkthrough, Technical review, Onboarding call) → enter a date (`YYYY-MM-DD`) → choose a time slot → receive a confirmation card with booking ID.
4. **`/support`** — Choose a category (Billing, Technical, Account, Integration, Other) → describe the issue → set priority (Low / Normal / Urgent) → receive a ticket ID.
5. **`/ai`** — Ask a product or troubleshooting question; the assistant remembers recent messages in your session.
6. **`/faq`** — Browse 8 categories or type a question (try searching for *whatsapp* or *discord* for cross-platform notes).
7. **`/about`** — Background on the demo and the patterns it showcases.

**Suggested order:** `/review` → `/book` → `/support` → `/ai`

---

## Tech stack

Python, python-telegram-bot, FastAPI, SQLite, Groq/OpenAI

---

## Author

**Zachary Hutton** — Portmore, Jamaica  
Portfolio: [zachary-hutton-portfolio.vercel.app](https://zachary-hutton-portfolio.vercel.app/)  
GitHub: [github.com/zacharyahutton/telegram-bot-demo](https://github.com/zacharyahutton/telegram-bot-demo)

---

Developer setup: see [DEPLOY.md](./DEPLOY.md)
