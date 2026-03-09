---
name: ask-oios
description: Answer any natural language question about the business using real data. The owner's go-to for quick business intelligence.
---

# Ask OIOS

Natural language query handler — the owner asks, OIOS answers from real data.

## Trigger
- Any question about the business
- "How many leads this week?"
- "What's my close rate?"
- "How much revenue this month?"
- "Who's my biggest customer?"
- "Any proposals about to expire?"
- "How's my pipeline looking?"
- "What jobs are scheduled this week?"

## Process

### Step 1: Parse the question
Identify:
- What data is needed (leads, pipeline, jobs, revenue, etc.)
- Time range (today, this week, this month, all-time)
- Specific filters (customer name, service type, status)

### Step 2: Read relevant data
Based on the question, read from:
- `contacts/` — customer/lead data
- `pipeline/` — deal data
- `jobs/` — job data
- `calls/` — call logs
- `proposals/` — proposal data
- `follow-ups/pending.jsonl` — follow-up queue
- `briefings/` — historical reports

### Step 3: Calculate the answer
- Count, sum, average, filter as needed
- Cross-reference files for complex queries
- Always use actual data — NEVER fabricate or estimate without flagging it

### Step 4: Respond
Keep it concise. Lead with the number/answer.

Examples:
- "12 leads this week — 3 A-grade, 5 B-grade, 4 C-grade"
- "Close rate: 42% (5 won, 7 lost) — up from 35% last week"
- "$18,500 in pipeline across 6 active deals"
- "3 jobs scheduled this week: [Customer1] Mon, [Customer2] Wed, [Customer3] Fri"

### Step 5: Offer follow-up
If the answer reveals something actionable:
- "Want me to follow up on those 3 stale proposals?"
- "Should I draft a re-engagement message for the cold leads?"

## Output
- Concise answer via Telegram
- Offer to take action if relevant

## Notes
- If data doesn't exist or is incomplete, say so — never guess
- For complex queries, break the answer into bullet points
- If the owner asks about something OIOS doesn't track, suggest adding it
