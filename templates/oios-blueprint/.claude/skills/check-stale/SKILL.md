---
name: check-stale
description: Find stale deals and overdue follow-ups. Runs daily at 10 AM or on demand.
---

# Check Stale

Scan for deals and follow-ups that are going cold.

## Trigger
- Daily cron at 10:00 AM
- "Check for stale deals"
- "Anything falling through the cracks?"

## Process

### Step 1: Scan active pipeline
Read all files in `pipeline/active/`. Flag any where:
- Proposal sent 3+ days ago with no status update
- No follow-up scheduled
- Estimated value > $2,000 (high-priority stale)

### Step 2: Scan overdue follow-ups
Read `follow-ups/pending.jsonl`. Flag entries where:
- `next_date` < today
- `status` == "pending"

### Step 3: Check for orphaned leads
Scan `contacts/leads/` for leads older than 7 days with:
- No pipeline entry (never got a proposal)
- No follow-up in queue

### Step 4: Generate recommendations
For each stale item, suggest an action:
- Stale proposal → "Send a follow-up or call"
- Overdue follow-up → "Draft message now"
- Orphaned lead → "Qualify or archive"

### Step 5: Alert owner
If any stale items found:
```
ALERT: [X] items need attention

Stale deals: [N]
- [Deal name] — $[value] — [days] days since proposal

Overdue follow-ups: [N]
- [Contact name] — [type] — [days] days overdue

Orphaned leads: [N]
- [Lead name] — no proposal or follow-up

Want me to draft follow-ups for these?
```

If nothing stale: no alert (don't spam).

## Output
- Telegram alert with stale items (only if found)
- Recommended actions for each item
