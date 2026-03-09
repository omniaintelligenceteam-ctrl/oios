---
name: answer-call
description: Handle post-call actions — draft confirmation to caller, alert on-call tech if urgent. Use after log-call processes an inbound call.
---

# Answer Call

Post-call automation — confirm with the caller and route urgent requests.

## Trigger
- Runs after `log-call` completes
- "Send a confirmation to the caller"
- "Handle the follow-up for this call"

## Process

### Step 1: Read the lead
Read the newly created lead file from `contacts/leads/`.

### Step 2: Draft confirmation text
Draft a short text message to the caller:
- Thank them for calling [COMPANY_NAME]
- Confirm what they need (service type)
- If appointment booked: confirm date/time
- If no appointment: let them know someone will follow up within [timeframe]
- Keep it under 160 characters if possible

### Step 3: Check urgency
If urgency is "urgent" or "emergency":
- Read `context/team.md` to find on-call tech
- Draft alert message with: customer name, location, issue, urgency level
- Present both messages to owner for approval

### Step 4: Present for approval
Send to owner via Telegram:
```
FOLLOW-UP: Ready to send for [Caller Name]

Text to caller:
"[Draft message]"

[If urgent] Alert to [Tech Name]:
"[Alert message]"

Approve? (yes/edit/skip)
```

### Step 5: Log action
Record in the lead's history what was sent and when.

## Output
- Draft confirmation text (pending owner approval)
- Urgent alert to on-call tech (if applicable)
- All actions logged in lead history

## Notes
- NEVER send without owner approval
- Keep texts professional but friendly — match voice.md tone
