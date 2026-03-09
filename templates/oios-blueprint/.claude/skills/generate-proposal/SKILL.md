---
name: generate-proposal
description: Generate a professional proposal for a lead or customer. Use when asked to create a proposal, quote, or bid.
---

# Generate Proposal

Create a professional proposal from lead/job data and the proposal template.

## Trigger
- "Generate a proposal for [name]"
- "Write up a quote for [customer]"
- After a qualified lead comes in (A or B grade)

## Process

### Step 1: Gather information
Read:
- Lead/customer file from `contacts/`
- `context/services.md` for pricing and service details
- `proposals/_template.md` for format

### Step 2: Build the proposal
Fill in the template with:
- Client name and details from contact file
- Scope of work based on service requested
- Pricing from `context/services.md` (adjust based on job specifics)
- Timeline estimate
- Standard terms from template

### Step 3: Save proposal
Save to `proposals/YYYY-MM-DD-customer-name.md`

### Step 4: Create pipeline entry
Create deal file in `pipeline/active/YYYY-MM-DD-customer-name.md`:
- Link to contact file
- Link to proposal
- Status: quoted
- Estimated value

### Step 5: Schedule follow-up
Add to `follow-ups/pending.jsonl`:
- Stage 1 follow-up in 3 days
- Type: post-quote

### Step 6: Send for review
Telegram to owner:
```
PROPOSAL: Draft ready for [Customer Name]
Service: [Service type]
Value: $[Amount]
File: proposals/[filename]

Review and approve?
```

## Output
- Proposal in `proposals/`
- Pipeline entry in `pipeline/active/`
- Follow-up scheduled
- Owner notified via Telegram
