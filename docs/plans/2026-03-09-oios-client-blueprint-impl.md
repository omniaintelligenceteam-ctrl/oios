# OIOS Client Blueprint — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the complete OIOS client blueprint — the productized folder structure, CLAUDE.md, skills, crons, and templates that get deployed to each client's OpenClaw instance on day one.

**Architecture:** Client gets their own Claude Code + OpenClaw instance. Pre-built skeleton with context files, file-based CRM, 10 skills across 3 pillars, 6 crons, and a self-improvement pipeline. Client interacts via Telegram. Wes manages backend via Claude Code.

**Tech Stack:** Claude Code, OpenClaw, Retell AI (voice only), Telegram Bot API

**Design Doc:** `docs/plans/2026-03-09-oios-client-blueprint-design.md`

**Existing Assets to Reuse:**
- `templates/client-onboarding/` — L0-L4 context templates (adapt, don't duplicate)
- `self-improver/engine.py` — Copy into blueprint as-is
- `.claude/skills/follow-up/SKILL.md` — Reference for skill format (YAML frontmatter + markdown)

---

## Task 1: Create Blueprint Directory Structure

**Files:**
- Create: `templates/oios-blueprint/` and all subdirectories

**Step 1: Create the full directory tree**

```bash
cd "c:/Users/default.DESKTOP-ON29PVN/OneDrive/Pictures/New folder/Wes EA"

# Root folders
mkdir -p templates/oios-blueprint/context
mkdir -p templates/oios-blueprint/contacts/customers
mkdir -p templates/oios-blueprint/contacts/leads
mkdir -p templates/oios-blueprint/contacts/vendors
mkdir -p templates/oios-blueprint/pipeline/active
mkdir -p templates/oios-blueprint/pipeline/won
mkdir -p templates/oios-blueprint/pipeline/lost
mkdir -p templates/oios-blueprint/jobs/scheduled
mkdir -p templates/oios-blueprint/jobs/in-progress
mkdir -p templates/oios-blueprint/jobs/completed
mkdir -p templates/oios-blueprint/calls
mkdir -p templates/oios-blueprint/proposals
mkdir -p templates/oios-blueprint/briefings
mkdir -p templates/oios-blueprint/follow-ups
mkdir -p templates/oios-blueprint/archives

# Skills (one folder per skill)
mkdir -p templates/oios-blueprint/.claude/skills/log-call
mkdir -p templates/oios-blueprint/.claude/skills/score-lead
mkdir -p templates/oios-blueprint/.claude/skills/answer-call
mkdir -p templates/oios-blueprint/.claude/skills/generate-proposal
mkdir -p templates/oios-blueprint/.claude/skills/follow-up
mkdir -p templates/oios-blueprint/.claude/skills/schedule-job
mkdir -p templates/oios-blueprint/.claude/skills/check-stale
mkdir -p templates/oios-blueprint/.claude/skills/daily-briefing
mkdir -p templates/oios-blueprint/.claude/skills/weekly-report
mkdir -p templates/oios-blueprint/.claude/skills/ask-oios

# Self-improver
mkdir -p templates/oios-blueprint/self-improver
```

**Step 2: Add .gitkeep files to empty directories**

```bash
for dir in customers leads vendors active won lost scheduled in-progress completed calls briefings archives; do
  find templates/oios-blueprint -type d -name "$dir" -exec touch {}/.gitkeep \;
done
```

**Step 3: Verify structure**

```bash
find templates/oios-blueprint -type d | sort
```

Expected: ~30 directories matching the design doc structure.

---

## Task 2: Create CLAUDE.md (The Brain)

**Files:**
- Create: `templates/oios-blueprint/CLAUDE.md`

**Step 1: Write the client CLAUDE.md**

This is the most critical file — it defines the entire OIOS personality, capabilities, and rules. Use `[PLACEHOLDERS]` for client-specific data.

Key sections:
1. **Identity** — "You are OIOS, the AI operations manager for [COMPANY_NAME]."
2. **Context references** — All @context/ files
3. **Capabilities** — What OIOS can do (query data, draft proposals, manage follow-ups, generate briefings)
4. **Boundaries** — What requires owner approval (external comms, scheduling, pricing, finances)
5. **Telegram behavior** — Short responses, category prefixes (LEAD, ALERT, BRIEFING), markdown formatting
6. **Data locations** — Where to find contacts, pipeline, jobs, calls, proposals
7. **Self-improvement** — Log corrections to self-improver/lessons-queue.jsonl
8. **Never do** — Never send external messages without approval, never delete data, never fabricate numbers

**Step 2: Verify** — Read through and confirm all placeholders are clearly marked with `[BRACKETS]`.

---

## Task 3: Create Context Templates

**Files:**
- Create: `templates/oios-blueprint/context/company.md`
- Create: `templates/oios-blueprint/context/voice.md`
- Create: `templates/oios-blueprint/context/services.md`
- Create: `templates/oios-blueprint/context/goals.md`
- Create: `templates/oios-blueprint/context/priorities.md`
- Create: `templates/oios-blueprint/context/team.md`
- Create: `templates/oios-blueprint/context/tools.md`
- Create: `templates/oios-blueprint/context/LAYERS.md`

**Step 1: Create company.md (L0)**

Adapt from `templates/client-onboarding/L0-identity.md`. Add YAML frontmatter. Fields: name, role, company, industry, timezone, location, what they do, #1 priority, company size, annual revenue.

**Step 2: Create voice.md (L0)**

Adapt from `templates/client-onboarding/L0-communication.md`. Fields: how OIOS should talk to the owner, how OIOS should talk to customers on behalf of the company, email signature, response timeframes, words/phrases to use or avoid.

**Step 3: Create services.md (L1)**

Adapt from `templates/client-onboarding/L1-business.md`. Fields: services offered (with pricing), service area, equipment/specialties, ideal customer profile, competitive differentiators.

**Step 4: Create goals.md (L1)**

Adapt from `templates/client-onboarding/L1-goals.md`. Fields: quarterly revenue target, growth goals, operational goals, key metrics to track.

**Step 5: Create priorities.md (L2)**

Adapt from `templates/client-onboarding/L2-priorities.md`. Fields: top 3-5 current priorities (updated weekly by OIOS or owner).

**Step 6: Create team.md (L2)**

Adapt from `templates/client-onboarding/L2-team.md`. Fields: name, role, phone, email, schedule, notes (per team member).

**Step 7: Create tools.md (L2)**

Adapt from `templates/client-onboarding/L2-tools.md`. Fields: CRM, accounting, scheduling, phone system, OIOS integrations, credential storage notes.

**Step 8: Create LAYERS.md**

Copy and adapt from `templates/client-onboarding/LAYERS.md`. Same 5-layer hierarchy but with OIOS-specific file names.

---

## Task 4: Create CRM Templates

**Files:**
- Create: `templates/oios-blueprint/contacts/_template.md`
- Create: `templates/oios-blueprint/pipeline/_template.md`
- Create: `templates/oios-blueprint/jobs/_template.md`
- Create: `templates/oios-blueprint/proposals/_template.md`
- Create: `templates/oios-blueprint/follow-ups/pending.jsonl` (empty file)

**Step 1: Contact template**

Fields: name, company, phone, email, address, type (customer/lead/vendor), source (call/referral/web), first contact date, notes, tags, lead score (if lead), jobs history (if customer).

**Step 2: Pipeline/deal template**

Fields: deal name, customer (link to contact), service requested, estimated value, status (quoted/negotiating/pending), proposal date, follow-up dates, close date, win/loss reason, notes.

**Step 3: Job template**

Fields: job name, customer (link to contact), deal (link to pipeline), scope, crew assigned, scheduled date, status (scheduled/in-progress/completed), special notes, completion date, revenue.

**Step 4: Proposal template**

Fields: client name, date, project title, scope of work, pricing (line items + total), timeline, terms & conditions, signature block. Use `[COMPANY_BRANDING]` placeholder for header/logo.

**Step 5: Create empty pending.jsonl**

Touch the file. Add a comment line or leave empty. This is where follow-up entries will be appended.

JSONL entry format (document in a comment at top):
```json
{"id": 1, "contact": "contacts/leads/mike-torres.md", "type": "post-quote", "stage": 1, "next_date": "2026-03-12", "channel": "text", "status": "pending", "notes": "Sent proposal 3/9, follow up in 3 days"}
```

---

## Task 5: Create Pillar 1 Skills — AI Receptionist

**Files:**
- Create: `templates/oios-blueprint/.claude/skills/log-call/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/score-lead/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/answer-call/SKILL.md`

**Step 1: log-call skill**

Trigger: When Retell webhook delivers call data, or when owner pastes a call transcript.
Process:
1. Extract: caller name, phone, property/location, service needed, urgency level, equipment details, estimated job value
2. Create lead file at `contacts/leads/YYYY-MM-DD-firstname-lastname.md` using contact template
3. Run score-lead on the new lead
4. Add follow-up entry to `follow-ups/pending.jsonl` (Day 1 follow-up)
5. Log call to `calls/YYYY-MM-DD-firstname-lastname.md` with full transcript + extracted data
6. Alert owner via Telegram: "LEAD: [Name] — [Service needed] — Score: [X]/100"

**Step 2: score-lead skill**

Trigger: Called by log-call, or manually ("score this lead").
Process:
1. Read lead file
2. Score 0-100 based on: estimated job value (0-30pts), urgency (0-25pts), service fit (0-25pts), commercial vs residential (0-20pts)
3. Assign grade: A (80+), B (60-79), C (40-59), D (<40)
4. Update lead file with score and grade
5. If A-grade: flag for immediate follow-up

**Step 3: answer-call skill**

Trigger: Post-call automation — runs after log-call.
Process:
1. Read the newly created lead file
2. Draft confirmation text to caller (short, professional, includes appointment details if booked)
3. If urgent: alert on-call tech with details
4. Create calendar reminder for follow-up
5. Present all drafts to owner for approval before sending

---

## Task 6: Create Pillar 2 Skills — AI Back Office

**Files:**
- Create: `templates/oios-blueprint/.claude/skills/generate-proposal/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/follow-up/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/schedule-job/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/check-stale/SKILL.md`

**Step 1: generate-proposal skill**

Trigger: "Generate a proposal for [lead/customer]", or after a qualified lead comes in.
Process:
1. Read lead/customer file from contacts/
2. Read `proposals/_template.md`
3. Fill in: scope based on service requested, pricing based on context/services.md, timeline, terms
4. Save to `proposals/YYYY-MM-DD-customer-name.md`
5. Create pipeline entry in `pipeline/active/`
6. Send draft to owner via Telegram for review/approval
7. Add Day 3 follow-up to pending.jsonl

**Step 2: follow-up skill**

Trigger: Daily cron (9 AM), or "follow up with [contact]".
Process:
1. Read `follow-ups/pending.jsonl`
2. Filter for entries where next_date <= today and status == "pending"
3. For each due follow-up:
   - Read the contact file
   - Draft message based on stage (Day 1, 3, 7, 14, 30 cadence)
   - Present draft to owner via Telegram
   - If approved: mark as sent, schedule next stage
   - If no more stages: mark as completed
4. Report: "FOLLOW-UP: X messages ready for approval"

**Step 3: schedule-job skill**

Trigger: "Schedule a job for [customer]", or when a deal is marked won.
Process:
1. Read deal from pipeline/active/
2. Create job file in `jobs/scheduled/` with: customer info, scope, crew, date, notes
3. Move deal from `pipeline/active/` to `pipeline/won/`
4. Update customer file in contacts/ (add to jobs history)
5. Alert owner: "JOB SCHEDULED: [Customer] — [Date] — [Crew]"

**Step 4: check-stale skill**

Trigger: Daily cron (10 AM), or "check for stale deals".
Process:
1. Scan `pipeline/active/` — find proposals older than 3 days without status update
2. Scan `follow-ups/pending.jsonl` — find overdue entries (next_date < today)
3. For each stale item, draft a recommended action
4. Alert owner: "ALERT: X stale deals, Y overdue follow-ups. [Details]"

---

## Task 7: Create Pillar 3 Skills — AI Command Center

**Files:**
- Create: `templates/oios-blueprint/.claude/skills/daily-briefing/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/weekly-report/SKILL.md`
- Create: `templates/oios-blueprint/.claude/skills/ask-oios/SKILL.md`

**Step 1: daily-briefing skill**

Trigger: 6:30 AM cron, or "give me my briefing".
Process:
1. Scan `jobs/scheduled/` — what's on the calendar today
2. Scan `follow-ups/pending.jsonl` — what follow-ups are due
3. Scan `contacts/leads/` — any new leads since last briefing
4. Scan `pipeline/active/` — pipeline summary (count, total value)
5. Check for any alerts (stale deals, overdue items)
6. Format as concise Telegram message:
   ```
   BRIEFING — [Date]

   Jobs today: X
   Follow-ups due: Y
   New leads: Z
   Pipeline: $XX,XXX (N deals)

   Needs attention: [if any]
   ```
7. Save to `briefings/YYYY-MM-DD.md`

**Step 2: weekly-report skill**

Trigger: Friday 4 PM cron, or "weekly report".
Process:
1. Scan all data folders for the past 7 days
2. Calculate metrics:
   - Leads captured (count + sources)
   - Proposals sent (count + total value)
   - Deals won/lost (count + value + close rate)
   - Jobs completed (count + revenue)
   - Follow-ups sent
   - Call answer rate (if Retell data available)
3. Compare to previous week (read last week's report from briefings/)
4. Format as detailed Telegram message + save to `briefings/YYYY-MM-DD-weekly.md`
5. Include trend indicators (up/down arrows) and recommended actions

**Step 3: ask-oios skill**

Trigger: Any natural language question about the business.
Process:
1. Parse the question to identify what data is needed
2. Read relevant files (contacts/, pipeline/, jobs/, calls/, briefings/)
3. Calculate answer from actual data (never fabricate)
4. Respond concisely via Telegram
5. Common queries to handle:
   - "How many leads this week/month?"
   - "What's my close rate?"
   - "How much revenue this month?"
   - "Who's my biggest customer?"
   - "Any proposals about to expire?"
   - "How's my pipeline looking?"
   - "What jobs are scheduled this week?"

---

## Task 8: Create Self-Improver + Cron Configs

**Files:**
- Create: `templates/oios-blueprint/self-improver/lessons-queue.jsonl` (empty)
- Copy: `templates/oios-blueprint/self-improver/engine.py` (from existing `self-improver/engine.py`)
- Create: `templates/oios-blueprint/CRONS.md` (cron documentation — OpenClaw will read this)

**Step 1: Copy self-improver**

Copy `self-improver/engine.py` to `templates/oios-blueprint/self-improver/engine.py`. Create empty `lessons-queue.jsonl`.

**Step 2: Create CRONS.md**

Document all 6 crons with their schedules, skills, and expected output. This file tells whoever sets up the OpenClaw instance what crons to configure:

| Cron | Schedule | Skill/Action | Output |
|------|----------|-------------|--------|
| Morning Briefing | 6:30 AM daily | `/daily-briefing` | Telegram to owner |
| Follow-Up Runner | 9:00 AM daily | `/follow-up` | Draft messages for approval |
| Stale Deal Check | 10:00 AM daily | `/check-stale` | Alert if stale deals found |
| End of Day Wrap | 5:00 PM daily | Scan today's activity, archive completed jobs | Activity log |
| Weekly Report | Friday 4:00 PM | `/weekly-report` | Full week summary |
| License Watch | Monday 8:00 AM | Check context/tools.md for upcoming expirations | Alert if any due |

---

## Task 9: Create Blueprint README + Deploy Script

**Files:**
- Create: `templates/oios-blueprint/README.md`

**Step 1: Write README**

The README is the deployment guide. It tells Wes (or future team) exactly how to deploy OIOS for a new client:

1. **Copy blueprint** — Copy `templates/oios-blueprint/` to the client's new repo
2. **Fill context files** — Walk through each file in `context/`, fill in client data from discovery call
3. **Customize templates** — Update proposal template with client branding, contact template with industry fields
4. **Set up Retell AI** — Configure voice agent with client's business name, hours, services
5. **Set up Telegram bot** — Create bot, connect to owner's Telegram
6. **Configure crons** — Set up all 6 crons in OpenClaw per CRONS.md
7. **Test the loop** — Simulate a call → lead → proposal → follow-up → briefing
8. **Go live** — Activate crons, hand off to owner

Include a checklist version for quick reference.

---

## Task 10: Verify + Final Review

**Step 1: Verify all files exist**

```bash
find templates/oios-blueprint -type f | sort
```

Expected: ~25-30 files (CLAUDE.md, 8 context files, 4 CRM templates, 10 skill files, CRONS.md, README.md, self-improver files, pending.jsonl).

**Step 2: Read through CLAUDE.md end-to-end**

Verify it's coherent, all context references work, boundaries are clear, no contradictions.

**Step 3: Check all skills have consistent format**

Each SKILL.md should have: YAML frontmatter (name, description), trigger section, process section with numbered steps.

**Step 4: Verify all placeholders are clearly marked**

Search for `[` in all files — every placeholder should be obvious fill-in-the-blank.

```bash
grep -r "\[" templates/oios-blueprint --include="*.md" | grep -v "node_modules" | head -40
```

---

## Summary

| Task | What | Files Created |
|------|------|--------------|
| 1 | Directory structure | ~30 directories |
| 2 | CLAUDE.md (the brain) | 1 file |
| 3 | Context templates | 8 files |
| 4 | CRM templates | 5 files |
| 5 | Pillar 1 skills (Receptionist) | 3 skills |
| 6 | Pillar 2 skills (Back Office) | 4 skills |
| 7 | Pillar 3 skills (Command Center) | 3 skills |
| 8 | Self-improver + crons | 3 files |
| 9 | README deploy guide | 1 file |
| 10 | Verify everything | 0 files (review) |

**Total: ~30 files across 10 tasks.**
