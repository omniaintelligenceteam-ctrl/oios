---
name: weekly-report
description: Generate a full weekly performance report with metrics, trends, and recommendations. Runs Friday at 4 PM or on demand.
---

# Weekly Report

Comprehensive weekly business performance review.

## Trigger
- Friday cron at 4:00 PM
- "Weekly report", "How'd we do this week?"
- "Give me the numbers"

## Process

### Step 1: Gather data for the past 7 days
Scan all data folders:
- `contacts/leads/` — new leads this week
- `pipeline/active/`, `pipeline/won/`, `pipeline/lost/` — deal activity
- `jobs/scheduled/`, `jobs/completed/` — job activity
- `proposals/` — proposals sent
- `follow-ups/pending.jsonl` — follow-up activity
- `calls/` — call volume

### Step 2: Calculate metrics

| Metric | Calculation |
|--------|------------|
| Leads captured | Count of new files in contacts/leads/ this week |
| Lead sources | Group by source field |
| Proposals sent | Count of new proposals this week |
| Proposal value | Sum of estimated values |
| Deals won | Count moved to pipeline/won/ |
| Deals lost | Count moved to pipeline/lost/ |
| Close rate | Won / (Won + Lost) * 100 |
| Revenue booked | Sum of won deal values |
| Jobs completed | Count moved to jobs/completed/ |
| Follow-ups sent | Count with status "sent" this week |

### Step 3: Compare to last week
Read `briefings/YYYY-MM-DD-weekly.md` from last Friday.
Calculate deltas for each metric.

### Step 4: Generate insights
- What's working (highest performing lead source, best close rate service)
- What's not (stale deals, low follow-up rate, missed leads)
- Recommended actions for next week

### Step 5: Format and send
Telegram:
```
WEEKLY REPORT — Week of [Date]

Leads: [X] [up/down vs last week]
Proposals: [X] ($[Value])
Won: [X] ($[Value]) | Lost: [X]
Close rate: [X]%
Jobs completed: [X]
Revenue: $[X]

Top source: [Source]
Needs attention: [1-2 items]

Full report: briefings/[filename]
```

### Step 6: Save report
Save full report to `briefings/YYYY-MM-DD-weekly.md` with all metrics and analysis.

## Output
- Telegram summary
- Full report saved to `briefings/`

## Notes
- Use trend arrows (up/down) to show direction
- Always include comparison to previous week
- If it's the first week, note "baseline established" instead of comparisons
