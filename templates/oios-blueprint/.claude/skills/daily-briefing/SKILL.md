---
name: daily-briefing
description: Generate a morning briefing with today's schedule, pending follow-ups, and pipeline status. Runs daily at 6:30 AM or on demand.
---

# Daily Briefing

Morning summary of everything the owner needs to know today.

## Trigger
- Daily cron at 6:30 AM
- "Give me my briefing"
- "What's on today?"

## Process

### Step 1: Check today's schedule
Scan `jobs/scheduled/` for jobs with today's date.

### Step 2: Check follow-ups due
Read `follow-ups/pending.jsonl` for entries due today.

### Step 3: Check new leads
Scan `contacts/leads/` for any created since yesterday's briefing.

### Step 4: Pipeline snapshot
Scan `pipeline/active/`:
- Count of active deals
- Total estimated value
- Any deals needing attention

### Step 5: Check alerts
- Stale deals (from yesterday's check-stale, if any)
- Overdue items
- Anything flagged as urgent

### Step 6: Format and send
Telegram:
```
BRIEFING — [Day, Month Date]

Jobs today: [X]
[- Job 1: Customer — Service — Crew]

Follow-ups due: [Y]
[- Name — Stage N — Type]

New leads: [Z]
[- Name — Service — Score]

Pipeline: $[Total] ([N] deals)

[Needs attention: (if any)]
```

### Step 7: Save briefing
Save to `briefings/YYYY-MM-DD.md` for historical reference.

## Output
- Telegram morning briefing
- Saved to `briefings/` folder

## Notes
- Keep the Telegram message concise — details available on request
- If nothing notable, still send a brief "All clear" message
- Compare to yesterday's briefing for trend context
