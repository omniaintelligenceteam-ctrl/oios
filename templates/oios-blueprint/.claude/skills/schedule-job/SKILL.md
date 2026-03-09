---
name: schedule-job
description: Create a job entry when a deal is won. Use when a proposal is accepted or owner says to schedule work.
---

# Schedule Job

Convert a won deal into a scheduled job.

## Trigger
- "Schedule a job for [customer]"
- "They accepted the proposal"
- Deal marked as won

## Process

### Step 1: Read the deal
Read the deal file from `pipeline/active/`.

### Step 2: Create job file
Create `jobs/scheduled/YYYY-MM-DD-customer-name.md` using the job template:
- Customer info from contact file
- Scope from deal/proposal
- Crew assignment (check `context/team.md` for availability)
- Scheduled date
- Revenue amount

### Step 3: Move deal to won
Move the deal file from `pipeline/active/` to `pipeline/won/`.
Update status to "won" with close date.

### Step 4: Update customer record
If contact is in `contacts/leads/`, move to `contacts/customers/`.
Add job to their history table.

### Step 5: Alert owner
Telegram:
```
JOB SCHEDULED: [Customer Name]
Date: [Scheduled date]
Crew: [Assigned crew]
Value: $[Amount]
Scope: [Brief description]
```

## Output
- Job file in `jobs/scheduled/`
- Deal moved to `pipeline/won/`
- Customer record updated
- Owner notified
