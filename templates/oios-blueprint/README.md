# OIOS Client Blueprint — Deployment Guide

This is the OIOS (Omnia Intelligence Operating System) blueprint. It contains everything needed to deploy a fully operational AI operations manager for a service business client.

## What's Inside

```
├── CLAUDE.md           — The brain (identity, rules, capabilities)
├── context/            — 8 context files (company, voice, services, goals, priorities, team, tools, layers)
├── contacts/           — File-based CRM (customers, leads, vendors)
├── pipeline/           — Deal tracking (active, won, lost)
├── jobs/               — Job management (scheduled, in-progress, completed)
├── calls/              — Call logs from Retell AI
├── proposals/          — Generated proposals
├── briefings/          — Daily and weekly AI briefings
├── follow-ups/         — Follow-up queue (pending.jsonl)
├── .claude/skills/     — 10 pre-built skills across 3 pillars
├── self-improver/      — Correction logging + pattern detection
├── CRONS.md            — Cron schedule reference
└── archives/           — Never delete, always archive here
```

## Deployment Steps

### 1. Copy the blueprint
Copy this entire `oios-blueprint/` folder to the client's new Claude Code / OpenClaw repository.

### 2. Fill context files (Day 1 — Discovery Call)
Walk through each file in `context/` and fill in the `[PLACEHOLDERS]`:

- [ ] `context/company.md` — Company name, owner, industry, location, size
- [ ] `context/voice.md` — Communication style, email signature, response times
- [ ] `context/services.md` — Services offered, pricing, service area
- [ ] `context/goals.md` — Quarterly targets and key metrics
- [ ] `context/priorities.md` — Current top 3-5 priorities
- [ ] `context/team.md` — Employee roster with roles and schedules
- [ ] `context/tools.md` — Existing software stack and integrations

### 3. Customize CLAUDE.md (Day 1)
Replace all `[PLACEHOLDERS]` in CLAUDE.md:
- [ ] `[COMPANY_NAME]` — Client's company name
- [ ] `[OWNER_NAME]` — Client owner's name

### 4. Customize templates (Days 2-3)
- [ ] `proposals/_template.md` — Add client branding, standard terms, pricing
- [ ] `contacts/_template.md` — Add industry-specific fields if needed

### 5. Set up Retell AI (Days 2-3)
- [ ] Create Retell AI agent with client's business name
- [ ] Configure business hours, services menu, greeting
- [ ] Set up webhook to trigger `log-call` skill
- [ ] Test with 3-5 sample calls

### 6. Set up Telegram bot (Days 2-3)
- [ ] Create bot via @BotFather on Telegram
- [ ] Connect bot to OpenClaw
- [ ] Add owner's Telegram as the primary recipient
- [ ] Test message delivery (briefing format, alerts)

### 7. Configure crons (Days 4-5)
Set up all 6 crons per `CRONS.md`:
- [ ] Morning Briefing — 6:30 AM daily
- [ ] Follow-Up Runner — 9:00 AM daily
- [ ] Stale Deal Check — 10:00 AM daily
- [ ] End of Day Wrap — 5:00 PM daily
- [ ] Weekly Report — Friday 4:00 PM
- [ ] License Watch — Monday 8:00 AM

### 8. Test the full loop (Days 4-5)
Run through the complete workflow:
- [ ] Simulate an inbound call → `log-call` creates lead
- [ ] Lead gets scored → `score-lead` assigns grade
- [ ] Post-call actions → `answer-call` drafts confirmation
- [ ] Generate proposal → `generate-proposal` creates proposal
- [ ] Follow-up triggers → `follow-up` drafts messages
- [ ] Morning briefing → `daily-briefing` sends summary
- [ ] Schedule a job → `schedule-job` creates job entry
- [ ] Weekly report → `weekly-report` generates metrics

### 9. Go live (Week 2)
- [ ] Activate all crons
- [ ] Port client's phone number to Retell AI (or set up forwarding)
- [ ] Train owner on Telegram interaction (how to approve, ask questions)
- [ ] Monitor first week of live operation

### 10. Optimize (Week 3+)
- [ ] Review `self-improver/lessons-queue.jsonl` for patterns
- [ ] Adjust scoring weights based on actual conversion data
- [ ] Fine-tune follow-up cadence based on response rates
- [ ] Add client-specific workflows as needed

## Quick Reference

| Pillar | Skills | What It Handles |
|--------|--------|----------------|
| AI Receptionist | log-call, score-lead, answer-call | Inbound calls, lead capture, qualification |
| AI Back Office | generate-proposal, follow-up, schedule-job, check-stale | Proposals, follow-ups, scheduling, stale alerts |
| AI Command Center | daily-briefing, weekly-report, ask-oios | Briefings, reports, natural language queries |

## Timeline Summary

| Phase | Duration | What Happens |
|-------|----------|-------------|
| Discovery | Day 1 | Fill context files from owner interview |
| Configure | Days 2-5 | Retell AI, Telegram, templates, crons |
| Test | Days 4-5 | Full loop simulation |
| Go Live | Week 2 | Activate everything, monitor |
| Optimize | Week 3+ | Tune based on real data |

## Notes
- **Never delete files** — always move to `archives/`
- **Never send external messages** without owner approval
- The system gets smarter over time via `self-improver/`
- All times in crons should be set to the client's timezone
