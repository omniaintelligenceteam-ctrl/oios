# OIOS Client Blueprint Design

**Date:** 2026-03-09
**Status:** Approved
**Decision:** Build the full OIOS client blueprint — the productized folder structure, CLAUDE.md, skills, crons, and templates that get deployed to each client's OpenClaw instance.

---

## What Is It

OIOS = a pre-built AI operating system deployed to a client's own Claude Code + OpenClaw instance. Client talks to it via Telegram. Wes manages the backend. The system gets smarter every day as it learns the client's business.

## Key Decisions

- **Scope:** Full Operating System (not starter kit) — everything pre-loaded on day one
- **Client interface:** Telegram via OpenClaw bot — client texts OIOS like texting an assistant
- **Admin interface:** Wes uses Claude Code directly to configure, optimize, troubleshoot
- **Delivery model:** Core skeleton + customize — structure is pre-built, business data filled in during onboarding
- **Only external tool:** Retell AI for voice/phone (everything else runs on Claude Code + OpenClaw)

## Architecture

```
Client (Telegram) --> OpenClaw Bot --> Claude Code (skills, crons, context, file CRM)
Wes (Claude Code) --> Same instance (configure, optimize, troubleshoot)
Retell AI --> Inbound calls --> Webhook --> OpenClaw (logs call, triggers workflows)
```

## Folder Structure

```
oios-client/
├── CLAUDE.md                    # The brain — identity, rules, capabilities
├── context/
│   ├── company.md               # L0: Company name, industry, owner, timezone
│   ├── voice.md                 # L0: How OIOS talks to/for this client
│   ├── services.md              # L1: What they sell, pricing, service areas
│   ├── goals.md                 # L1: Quarterly targets
│   ├── priorities.md            # L2: Current focus (updated weekly)
│   ├── team.md                  # L2: Employees, roles, schedules
│   ├── tools.md                 # L2: Their existing software stack
│   └── LAYERS.md                # Reference: layer hierarchy
├── contacts/                    # File-based CRM
│   ├── customers/               # One .md per customer
│   ├── leads/                   # Incoming leads (auto-created from calls)
│   ├── vendors/                 # Suppliers, subcontractors
│   └── _template.md             # Contact template
├── pipeline/                    # Active deals
│   ├── active/                  # Open quotes/proposals
│   ├── won/                     # Closed deals (archived monthly)
│   ├── lost/                    # Lost deals (with reason)
│   └── _template.md             # Deal template
├── jobs/                        # Active work
│   ├── scheduled/               # Upcoming jobs
│   ├── in-progress/             # Currently being worked
│   ├── completed/               # Done (archived monthly)
│   └── _template.md             # Job template
├── calls/                       # Call logs from Retell AI
│   └── YYYY-MM-DD-caller.md     # Auto-generated per call
├── proposals/                   # Generated proposals
│   └── _template.md             # Proposal template
├── briefings/                   # Daily/weekly AI briefings
│   └── YYYY-MM-DD.md            # Auto-generated
├── follow-ups/                  # Scheduled follow-up queue
│   └── pending.jsonl            # JSONL queue of pending follow-ups
├── .claude/
│   └── skills/
│       ├── answer-call/         # Process inbound call data from Retell
│       ├── generate-proposal/   # Create proposal from lead/job data
│       ├── follow-up/           # Draft and send follow-up messages
│       ├── daily-briefing/      # Generate morning briefing
│       ├── weekly-report/       # Generate weekly performance report
│       ├── log-call/            # Log and extract data from call transcript
│       ├── score-lead/          # Score and qualify incoming leads
│       ├── schedule-job/        # Create job entry from won deal
│       ├── check-stale/         # Find proposals/follow-ups going cold
│       └── ask-oios/            # Natural language query handler
├── self-improver/
│   ├── lessons-queue.jsonl      # Correction log
│   └── engine.py                # Pattern detection
└── archives/                    # Never delete, always archive
```

## CLAUDE.md Design

The client's CLAUDE.md is the brain of their OIOS instance. It contains:

### Identity Section
- "You are OIOS, the AI operations manager for [Company Name]."
- "You report to [Owner Name]. They are your boss."
- "Your job is to keep the business running smoothly — capture every lead, follow up on everything, and keep [Owner] informed."

### Context References
- All @context/ files loaded every session
- LAYERS.md for update cadence

### Capabilities
- Answer questions about the business (pipeline, jobs, team, metrics)
- Draft and send follow-up messages (via Telegram, with owner approval)
- Generate proposals from templates
- Log and process incoming calls
- Generate daily briefings and weekly reports
- Score and qualify leads
- Track jobs from scheduled through completion
- Alert owner to stale deals, missed follow-ups, upcoming deadlines

### Boundaries (Require Human Approval)
- Sending any external communication (proposals, follow-ups, emails)
- Scheduling or canceling jobs
- Making pricing decisions
- Contacting customers directly
- Any financial transaction

### Telegram Behavior
- Keep responses short (under 300 chars for quick updates)
- Use markdown formatting
- Lead with the answer, then details if asked
- Proactive alerts: prefix with the category (LEAD, FOLLOW-UP, ALERT, BRIEFING)
- When asked a question, check relevant data files before answering

### Self-Improvement
- Log corrections to self-improver/lessons-queue.jsonl
- Learn owner's preferences over time
- Never repeat a corrected mistake

## Crons

| Cron | Schedule | Skill | Output |
|------|----------|-------|--------|
| Morning Briefing | 6:30 AM daily | daily-briefing | Telegram message to owner |
| Stale Deal Check | 10:00 AM daily | check-stale | Telegram alert if any found |
| Follow-Up Runner | 9:00 AM daily | follow-up | Draft messages for approval |
| Weekly Report | Friday 4:00 PM | weekly-report | Full week summary via Telegram |
| End of Day Wrap | 5:00 PM daily | (inline) | Activity log, move completed jobs |
| License Watch | Monday 8:00 AM | (inline) | Check for upcoming expirations |

## Skills Detail

### Pillar 1 — AI Receptionist

**log-call** — Retell webhook delivers call transcript. OIOS extracts: caller name, phone, property/location, service needed, urgency level, equipment details. Creates lead file in contacts/leads/. Triggers score-lead.

**score-lead** — Scores lead 0-100 based on: job value estimate, urgency, service fit, commercial vs residential. Assigns grade (A/B/C). Updates lead file.

**answer-call** — Post-call actions: sends confirmation text to caller, alerts on-call tech if urgent, creates CRM entry, sets calendar reminder for follow-up.

### Pillar 2 — AI Back Office

**generate-proposal** — Takes lead/job data + proposals/_template.md. Generates professional proposal with: scope, pricing, timeline, terms. Saves to proposals/ folder. Sends draft to owner for approval via Telegram.

**follow-up** — Processes follow-ups/pending.jsonl. Drafts follow-up messages based on cadence (Day 1, 3, 7, 14, 30). Sends drafts to owner via Telegram for approval before sending.

**schedule-job** — When a deal is marked won, creates job entry in jobs/scheduled/ with: customer info, scope, crew assignment, date, special notes. Moves deal from pipeline/active/ to pipeline/won/.

**check-stale** — Scans pipeline/active/ for proposals older than 3 days without response. Scans follow-ups/pending.jsonl for overdue items. Alerts owner via Telegram with recommended action.

### Pillar 3 — AI Command Center

**daily-briefing** — Generates morning summary: jobs scheduled today, follow-ups due, new leads overnight, pipeline status, any alerts. Delivered via Telegram at 6:30 AM.

**weekly-report** — Full week metrics: leads captured, proposals sent, close rate, jobs completed, revenue, team utilization, trends vs. last week. Delivered via Telegram Friday afternoon.

**ask-oios** — Natural language query handler. Owner asks anything about their business. OIOS reads relevant data files (contacts/, pipeline/, jobs/, calls/) and responds with accurate, current data. Examples: "How many leads this week?" "What's my close rate?" "Who's my biggest customer?" "Any proposals about to expire?"

## What Gets Customized During Onboarding

| File | Filled During | Source |
|------|--------------|--------|
| context/company.md | Discovery call | Owner interview |
| context/voice.md | Discovery call | Owner preferences |
| context/services.md | Discovery call + research | Owner + website |
| context/goals.md | Discovery call | Owner priorities |
| context/team.md | Onboarding | Owner provides roster |
| context/tools.md | Onboarding | Owner's existing stack |
| proposals/_template.md | Onboarding | Owner's branding/terms |
| contacts/_template.md | Onboarding | Industry-specific fields |
| Retell AI agent | Week 1 | Business name, hours, services |
| Telegram bot | Week 1 | Connected to owner's phone |

## Onboarding Timeline

- **Day 1:** Discovery call — fill L0 + L1 context files
- **Day 2-3:** Configure Retell AI voice agent, set up Telegram bot
- **Day 4-5:** Build proposal template, customize contact/job templates
- **Day 6-7:** Activate crons, test full loop (call → lead → proposal → follow-up)
- **Week 2:** Monitor, optimize, add any client-specific workflows
- **Week 3:** Full handoff, owner trained on Telegram interaction

## The Moat

The system accumulates business knowledge over time:
- Month 1: Handles calls, follow-ups, proposals
- Month 3: Knows customers, vendors, seasonal patterns
- Month 6: Basically their COO — impossible to rip out
- Month 12: Running the business better than any human admin

This accumulated context is the lock-in. After 6 months, switching away means losing everything OIOS has learned about their business.
