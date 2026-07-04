# Multi-platform bot strategy — Mindrift, portfolio, weROI

## Goal

One **core bot engine**, three **channel adapters**, three **business outcomes**:

| Outcome | Audience | Deliverable |
|---------|----------|-------------|
| **Get hired** | Mindrift / Tendem reviewers | Live Telegram bot + `/review` tour |
| **Portfolio proof** | Recruiters & clients | 3 case studies (Telegram, WhatsApp, Discord) |
| **weROI service** | SMB clients in Jamaica + remote | “Messaging Automation” add-on for agencies |

---

## What Mindrift/Tendem reviewers want to see

Map every demo feature to their posting:

| They ask for | Your demo proves it |
|--------------|---------------------|
| WhatsApp / Telegram / Discord | Telegram live; FAQ explains WA templates + Discord patterns |
| Conversational flows | `/book` multi-step, `/support` ticket with priority |
| LLM integration | `/ai` with Groq/OpenAI, memory, FAQ fallback |
| Webhooks & backend | FastAPI `/telegram/webhook`, secret token, `/health` |
| Production hardening | Rate limits, SQLite state, admin `/stats`, structured events |
| AI Pilot workflow | You built with AI assistance, documented edge cases, fail-loud design |

**Reviewer script:** Send `/review` in Telegram — 60-second checklist they can follow without reading README.

---

## Architecture (shared core)

```
                    ┌─────────────────────┐
                    │   bot/core/         │
                    │   flows, FAQ, LLM   │
                    │   database, events  │
                    └──────────┬──────────┘
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
   adapters/telegram    adapters/whatsapp   adapters/discord
   (done)               (next)              (next)
           │                   │                   │
           ▼                   ▼                   ▼
   FastAPI webhook      Meta Cloud API      discord.py gateway
```

**Refactor later:** Extract `bot/handlers/core.py` logic into platform-agnostic `flows/` when you add WhatsApp. For the application, Telegram + clear docs is enough.

---

## Build order (fastest impact)

### Phase 1 — Telegram 24/7 (this week) ✅ target

- [x] Flows, FAQ, LLM, SQLite, webhooks
- [ ] Railway deploy (`DEPLOY.md`)
- [ ] `/review` command for hiring panel
- [ ] Own GitHub repo + portfolio case study update
- [ ] Apply with live `t.me/…` link

### Phase 2 — WhatsApp demo (portfolio + “I can do Tendem”)

**Stack:** Meta WhatsApp Cloud API + same FastAPI app

**Minimum demo (1–2 days):**

- Webhook verification (`GET` challenge)
- Inbound text → same FAQ matcher + booking flow (button/list messages)
- One approved **template** for booking confirmation (proves you know WA constraints)
- README section: “Telegram vs WhatsApp differences”

**Portfolio title:** *WhatsApp Business Demo Bot — template flows & webhook verification*

**weROI angle:** “WhatsApp lead capture for Jamaican businesses” (restaurants, salons, clinics)

### Phase 3 — Discord demo (portfolio)

**Stack:** `discord.py` + slash commands mirroring `/book`, `/support`, `/faq`

**Minimum demo (1 day):**

- `/start`-equivalent slash commands
- Embed-based FAQ
- Thread for support tickets
- Same SQLite or shared Postgres

**Portfolio title:** *Discord Support Bot — slash commands & thread escalation*

### Phase 4 — weROI productized service

Package as **GrowthIQ Messaging** or **weROI Chat Automation**:

| Tier | Channels | Features |
|------|----------|----------|
| Starter | Telegram or WhatsApp | FAQ + business hours + contact capture |
| Growth | + LLM assistant | Groq/OpenAI, memory, human handoff |
| Pro | Multi-channel + CRM | Webhooks to HubSpot/Sheets, booking sync |

**Pricing idea (JMD / USD):** setup fee + monthly (hosting + API usage). Use your live demos as sales proof.

---

## Portfolio entries (when each ships)

| Project | Slug | Live proof |
|---------|------|------------|
| Tendem Demo Bot | `tendem-demo-bot` | `t.me/…` |
| WhatsApp Business Demo | `whatsapp-demo-bot` | Meta test number + screen recording |
| Discord Support Bot | `discord-support-bot` | Invite link to demo server |

All three share: Python, FastAPI, webhooks, LLM optional, GitHub monorepo or `zacharyahutton/bot-toolkit`.

---

## Honest framing (use in interviews)

> “My deepest live deployment is Telegram with FastAPI webhooks. I built WhatsApp and Discord demos using the same conversation core to show I understand platform-specific constraints — templates on WhatsApp, slash commands on Discord, secret tokens on Telegram. On Tendem I would ship production quality on whichever channel the client needs first.”

That is exactly what strong AI Pilot candidates say.

---

## Next actions for you

1. **Today:** Deploy Telegram to Railway (`DEPLOY.md`)
2. **Before apply:** Test `/review`, paste real bot link in cover letter
3. **This week:** Push `telegram-bot-demo` to its own GitHub repo
4. **After apply:** Start WhatsApp adapter (Meta developer account is free)
