---
name: follow-up
description: Process pending follow-ups and draft messages for owner approval. Runs daily at 9 AM or on demand.
---

# Follow-Up

Draft and manage follow-up messages on a timed cadence.

## Trigger
- Daily cron at 9:00 AM
- "Check follow-ups", "Any follow-ups due?"
- "Follow up with [name]"

## Process

### Step 1: Read the queue
Read `follow-ups/pending.jsonl`. Filter for entries where:
- `next_date` <= today
- `status` == "pending"

### Step 2: Draft messages for each due follow-up
For each due entry:
1. Read the linked contact file
2. Read `context/voice.md` for tone
3. Draft message based on stage and type:

**Post-call cadence:**
- Stage 1 (Day 1): Thank for calling, confirm next steps
- Stage 2 (Day 3): Quick check-in, add value
- Stage 3 (Day 7): Gentle nudge, easy yes/no question
- Stage 4 (Day 14): Last touch, leave door open

**Post-quote cadence:**
- Stage 1 (Day 3): Check if they have questions about the proposal
- Stage 2 (Day 7): Add social proof or relevant example
- Stage 3 (Day 14): Address common hesitations
- Stage 4 (Day 30): Breakup — keep the door open

### Step 3: Present to owner
Telegram message:
```
FOLLOW-UP: [X] messages ready

1. [Name] — [Type] Stage [N]
   "[Draft message preview]"

2. [Name] — [Type] Stage [N]
   "[Draft message preview]"

Approve all / Edit / Skip?
```

### Step 4: Process approvals
- Approved: mark as sent, schedule next stage
- Edited: send edited version, mark as sent, schedule next stage
- Skipped: keep in queue, bump next_date by 2 days
- Final stage completed: mark as "completed"

## Output
- Draft messages presented to owner
- Queue updated based on approvals

## Notes
- Never say "just checking in" or "circling back"
- Keep Stage 2+ messages under 100 words
- Be direct about what you want from them
- If a lead goes cold past Stage 4, mark as completed and note for 60-day re-engagement
