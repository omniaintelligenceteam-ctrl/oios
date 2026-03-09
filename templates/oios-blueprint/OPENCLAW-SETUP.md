# OpenClaw Setup Guide — OIOS Client Deployment

**Internal doc — for Wes only. Not client-facing.**

OpenClaw is the nervous system. It handles routing, scheduling, the Telegram bot, webhooks, and credential storage. Claude Code is the brain — all intelligence and data lives there. OpenClaw calls Claude Code skills and delivers results back to the client via Telegram.

---

## 1. Telegram Bot Setup

### Create the Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Name it: `[COMPANY_NAME] OIOS` (display name)
4. Username: `[company]_oios_bot` (must end in `bot`, must be unique)
5. Copy the **bot token** — you'll need it for OpenClaw

### Configure the Bot Profile

1. Send `/setdescription` to @BotFather — use:
   ```
   AI operations manager for [COMPANY_NAME]. Text me to check your pipeline, leads, jobs, and more.
   ```
2. Send `/setuserpic` — upload OIOS-branded profile photo
3. Send `/setcommands` — skip this (we use natural language, not slash commands)

### Connect to OpenClaw

1. In OpenClaw, create a new Telegram integration
2. Paste the bot token
3. Set the webhook URL: `https://[OPENCLAW_INSTANCE]/webhook/telegram/[CLIENT_ID]`
4. OpenClaw will confirm the webhook is active

### Connect to Owner

1. Have the client open the bot in Telegram and send any message (e.g., "hello")
2. This registers their Telegram user ID
3. Save their Telegram ID as `OWNER_TELEGRAM_ID` in OpenClaw env vars
4. All proactive messages (briefings, alerts) go to this ID

---

## 2. Webhook Configuration (Retell AI)

### Set Up the Endpoint

1. In OpenClaw, create a webhook endpoint:
   ```
   POST https://[OPENCLAW_INSTANCE]/webhook/retell/[CLIENT_ID]
   ```
2. Set a webhook secret for validation — save as `RETELL_WEBHOOK_SECRET`

### Configure Retell AI to Send Data

1. In the client's Retell AI agent settings, find the webhook/callback URL field
2. Paste the OpenClaw endpoint URL
3. Set the trigger to fire on **call ended**

### Expected Payload Format

Retell sends a JSON payload after each call. The fields OIOS cares about:

```json
{
  "call_id": "string",
  "from_number": "+15551234567",
  "to_number": "+15559876543",
  "duration_seconds": 180,
  "call_status": "completed",
  "transcript": "Full call transcript text...",
  "recording_url": "https://...",
  "metadata": {},
  "ended_at": "2026-03-09T14:30:00Z"
}
```

### Routing

When OpenClaw receives this payload, it:
1. Validates the webhook secret
2. Passes the payload to the `/log-call` skill in Claude Code
3. `/log-call` creates the lead file in `contacts/leads/`, logs to `calls/`, and scores the lead
4. If the lead scores 60+, sends a **LEAD:** alert to the owner via Telegram

---

## 3. Cron Jobs

Map each cron from `CRONS.md` into OpenClaw's scheduler. All times use `CLIENT_TIMEZONE`.

### OpenClaw Cron Configuration

| Name | Cron Expression | Skill | Notes |
|------|----------------|-------|-------|
| Morning Briefing | `30 6 * * *` | `/daily-briefing` | Sends Telegram summary every morning |
| Follow-Up Runner | `0 9 * * *` | `/follow-up` | Checks `follow-ups/pending.jsonl`, drafts messages |
| Stale Deal Check | `0 10 * * *` | `/check-stale` | Only sends alert if stale items found |
| End of Day Wrap | `0 17 * * *` | _(inline — see below)_ | Archives completed jobs, saves EOD summary |
| Weekly Report | `0 16 * * 5` | `/weekly-report` | Friday 4 PM — full week metrics |
| License Watch | `0 8 * * 1` | _(inline — see below)_ | Monday 8 AM — checks tool expirations |

### Setting Up Each Cron in OpenClaw

For each cron:
1. Create a new scheduled task in OpenClaw
2. Set the cron expression (see table above)
3. Set the timezone to `CLIENT_TIMEZONE`
4. For skill-based crons: point to the skill path (e.g., `/daily-briefing`)
5. For inline crons: paste the inline logic directly (see `CRONS.md` for the EOD Wrap and License Watch logic)
6. Set the output channel to Telegram (using the bot token and owner ID)

### Inline Cron Logic

**End of Day Wrap (5:00 PM daily):**
- Scan `jobs/in-progress/` — move completed jobs to `jobs/completed/`
- Count today's calls logged, proposals sent, follow-ups completed
- Save summary to `briefings/YYYY-MM-DD-eod.md`
- No Telegram message unless something unusual happened

**License Watch (Monday 8:00 AM):**
- Read `context/tools.md`
- Check for tools with expiration dates within 14 days
- If found: send Telegram alert `ALERT: [Tool] expires [date]`
- If nothing expiring: no message

---

## 4. Routing Rules

OpenClaw determines which skill to invoke based on message source and content.

### Message Routing Table

| Source | Trigger | Routes To | Description |
|--------|---------|-----------|-------------|
| Telegram (owner) | Any text message | `/ask-oios` | Natural language query — owner asks OIOS anything |
| Telegram (owner) | Message starts with `/propose` | `/generate-proposal` | Shortcut to generate a proposal |
| Telegram (owner) | Message starts with `/score` | `/score-lead` | Shortcut to score a specific lead |
| Telegram (owner) | Message starts with `/schedule` | `/schedule-job` | Shortcut to schedule a job |
| Webhook (Retell) | POST to retell endpoint | `/log-call` | Inbound call data from Retell AI |
| Cron | Scheduled time | Specific skill | See cron table above |

### Default Routing

- If OpenClaw can't determine a specific skill from the owner's message, default to `/ask-oios`
- `/ask-oios` is the catch-all — it reads the message, checks relevant data files, and responds
- All responses are delivered back through the Telegram bot

### Owner Command Shortcuts (Optional)

These are convenience shortcuts. The owner can also just ask in plain English and `/ask-oios` will handle it.

```
/briefing     → triggers /daily-briefing on demand
/pipeline     → triggers /ask-oios with "show me the pipeline"
/followups    → triggers /ask-oios with "what follow-ups are pending?"
/report       → triggers /weekly-report on demand
```

Configure these as keyword-based routes in OpenClaw if the client wants them.

---

## 5. Environment Variables

Set these in OpenClaw's environment/secrets configuration for each client instance.

```
# Telegram
TELEGRAM_BOT_TOKEN=          # From @BotFather (Section 1)
OWNER_TELEGRAM_ID=           # Owner's Telegram user ID (captured on first message)

# Retell AI
RETELL_WEBHOOK_SECRET=       # Secret for validating webhook payloads

# Client Config
CLIENT_TIMEZONE=             # e.g., America/Chicago, America/New_York
CLIENT_NAME=[COMPANY_NAME]   # Used in logs and error messages

# Claude Code
CLAUDE_CODE_PATH=            # Path to the client's Claude Code instance/repo
```

### Where to Find These Values

| Variable | Where to Get It |
|----------|----------------|
| `TELEGRAM_BOT_TOKEN` | @BotFather gives this when you create the bot |
| `OWNER_TELEGRAM_ID` | Check OpenClaw logs after the owner sends their first message |
| `RETELL_WEBHOOK_SECRET` | Generate a random string (32+ chars) and set it in both OpenClaw and Retell |
| `CLIENT_TIMEZONE` | Ask the client. Use IANA format (America/Chicago, not "Central") |

---

## 6. Testing Checklist

Run through every item before going live. Do NOT activate crons until all tests pass.

### Telegram Bot
- [ ] Bot is created and token is saved in OpenClaw
- [ ] Owner sent first message — Telegram ID captured
- [ ] Owner sends "How's my pipeline?" — gets a response from `/ask-oios`
- [ ] Bot responds within 10 seconds
- [ ] Response formatting looks clean (markdown renders properly)

### Webhook (Retell AI)
- [ ] Webhook endpoint is live and accepting POST requests
- [ ] Send a test payload (use curl or Retell's test feature)
- [ ] `/log-call` creates a lead file in `contacts/leads/`
- [ ] `/log-call` creates a call log in `calls/`
- [ ] Lead scoring runs and assigns a score
- [ ] If score is 60+, Telegram alert fires

### Cron Jobs
- [ ] Trigger `/daily-briefing` manually — check Telegram output
- [ ] Trigger `/follow-up` manually — check drafts (add a test entry to `pending.jsonl` first)
- [ ] Trigger `/check-stale` manually — verify it only alerts when stale items exist
- [ ] Trigger EOD Wrap manually — verify it saves to `briefings/`
- [ ] Trigger `/weekly-report` manually — check Telegram and file output
- [ ] Trigger License Watch manually — verify it reads `context/tools.md`
- [ ] Activate all crons and verify they fire at correct times (watch for 1 day)

### Routing
- [ ] Owner text message → `/ask-oios` responds
- [ ] Retell webhook → `/log-call` processes
- [ ] Each shortcut command routes correctly (if configured)
- [ ] Unknown/malformed input gets a graceful fallback response

### Error Handling
- [ ] Kill the Claude Code connection — OpenClaw sends a fallback message via Telegram: "OIOS is temporarily offline. Wes has been notified."
- [ ] Send a malformed webhook payload — no crash, error is logged
- [ ] Cron fires but skill fails — error logged, no silent failure

---

## Quick Reference: Full Setup Order

1. Create Telegram bot and get token
2. Set environment variables in OpenClaw
3. Connect Telegram webhook
4. Have owner message the bot (captures Telegram ID)
5. Set up Retell AI webhook endpoint
6. Configure Retell to POST to the endpoint
7. Test Telegram routing (owner message → response)
8. Test webhook (Retell payload → lead created)
9. Configure all 6 crons
10. Test each cron manually
11. Activate crons
12. Monitor for 24-48 hours before calling it live
