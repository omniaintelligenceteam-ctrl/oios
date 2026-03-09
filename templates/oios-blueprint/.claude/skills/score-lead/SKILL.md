---
name: score-lead
description: Score and qualify a lead from 0-100. Use after logging a call or when asked to evaluate a lead.
---

# Score Lead

Score incoming leads 0-100 to prioritize follow-up.

## Trigger
- Called automatically by `log-call`
- "Score this lead", "How hot is this lead?"
- Owner asks about lead quality

## Process

### Step 1: Read lead data
Read the lead file from `contacts/leads/`.

### Step 2: Calculate score (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Job value estimate | 0-30 | <$500: 5, $500-2K: 15, $2K-5K: 25, $5K+: 30 |
| Urgency | 0-25 | Routine: 5, Soon: 10, Urgent: 20, Emergency: 25 |
| Service fit | 0-25 | Core service: 25, Adjacent: 15, Outside expertise: 5 |
| Customer type | 0-20 | Commercial: 20, Residential high-end: 15, Residential standard: 10 |

### Step 3: Assign grade
- **A** (80-100): Hot lead — follow up immediately
- **B** (60-79): Warm lead — follow up within 24 hours
- **C** (40-59): Cool lead — follow up within 3 days
- **D** (0-39): Low priority — add to nurture sequence

### Step 4: Update lead file
Add `lead_score` and `lead_grade` to the YAML frontmatter.
Add scoring breakdown to the lead file body.

### Step 5: Flag A-grade leads
If grade is A, add note: "PRIORITY: A-grade lead — immediate follow-up recommended"

## Output
- Updated lead file with score and grade
- A-grade leads flagged for immediate action
