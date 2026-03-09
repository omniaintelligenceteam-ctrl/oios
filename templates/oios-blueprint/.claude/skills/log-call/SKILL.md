---
name: log-call
description: Log and extract data from an inbound call transcript. Use when Retell AI delivers call data or when the owner pastes a call transcript manually.
---

# Log Call

Process inbound call data — extract key details, create a lead, and trigger follow-up.

## Trigger
- Retell AI webhook delivers call transcript
- Owner pastes a call transcript or summary
- "Log this call", "I just got a call from..."

## Process

### Step 1: Extract call data
From the transcript, extract:
- Caller name
- Phone number
- Property/location address
- Service needed
- Urgency level (routine / soon / urgent / emergency)
- Equipment details (if mentioned)
- Estimated job value (based on service type + context/services.md pricing)
- Any special requests or notes

### Step 2: Create lead file
Create `contacts/leads/YYYY-MM-DD-firstname-lastname.md` using the contact template.
Fill in all extracted data. Set `type: lead`, `source: call`.

### Step 3: Score the lead
Run `/score-lead` on the new lead file.

### Step 4: Set up follow-up
Add entry to `follow-ups/pending.jsonl`:
```json
{"id": N, "contact": "contacts/leads/YYYY-MM-DD-firstname-lastname.md", "type": "post-call", "stage": 1, "next_date": "TOMORROW", "channel": "text", "status": "pending", "notes": "Initial follow-up after inbound call"}
```

### Step 5: Log the call
Save full call log to `calls/YYYY-MM-DD-firstname-lastname.md` with:
- Call timestamp
- Full transcript (if available)
- Extracted data summary
- Lead score result

### Step 6: Alert owner
Send Telegram message:
```
LEAD: [Name] — [Service needed]
Score: [X]/100 ([Grade])
Value: ~$[Estimate]
Next: Follow-up scheduled [date]
```

## Output
- New lead file in `contacts/leads/`
- Call log in `calls/`
- Follow-up entry in `follow-ups/pending.jsonl`
- Telegram alert to owner
