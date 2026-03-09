---
layer: L2-Operations
cadence: as-needed
description: Software tools and integrations
---

# Tools & Integrations

## Active Tools

### OIOS (This System)
- AI operations manager powered by Claude + OpenClaw
- Telegram bot for owner communication
- Retell AI for voice/phone handling

### [CRM_OR_FSM_TOOL]
- [What it does — e.g., job scheduling, invoicing]
- [How OIOS interacts with it — e.g., data sync, manual entry]

### [ACCOUNTING_TOOL]
- [e.g., QuickBooks, FreshBooks]
- [Integration notes]

### [SCHEDULING_TOOL]
- [e.g., Google Calendar, Jobber]
- [Integration notes]

### [PHONE_SYSTEM]
- Retell AI — handles inbound calls 24/7
- Webhook sends call data to OIOS for processing
- [Backup phone system if any]

## Credentials
- All credentials stored in `.env` (never in plain text files)
- Retell AI API key: configured in OpenClaw
- Telegram bot token: configured in OpenClaw

## Not Yet Integrated
- [Any tools the client uses that aren't connected yet]
