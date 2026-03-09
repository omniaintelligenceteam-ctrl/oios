---
name: form-fill
description: >
  Automated outreach to companies hiring for back-office roles (receptionist, office manager, admin).
  Scrapes job boards, finds company contact forms, fills and submits them with a personalized message
  pointing to silentaipartner.com. Logs all attempts to projects/form-fill/log.csv.
  Triggers on "fill forms", "contact companies", "outreach automation", "find companies hiring",
  or /form-fill.
---

# Form Fill Skill

## When to Use

Use when Wes wants to reach out to companies hiring for:
- Receptionist / front desk
- Office manager
- Admin assistant
- Back-office / operations
- Scheduling coordinator

These companies are signaling the exact pain OIOS solves.

## How to Run

```bash
cd "c:\Users\default.DESKTOP-ON29PVN\OneDrive\Pictures\New folder\Wes EA\.claude\skills\form-fill"
TWO_CAPTCHA_API_KEY=<from CLAUDE.local.md> python runner.py "<query>" --limit <n> --parallel <n>
```

**Examples:**
```bash
python runner.py "receptionist hiring" --limit 20 --parallel 5
python runner.py "office manager job" --limit 10 --parallel 3
python runner.py "admin assistant opening" --limit 50 --parallel 5
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| query | required | Job title to search for |
| --limit | 20 | Max companies to process |
| --parallel | 5 | Simultaneous browser agents |

## Output

- Real-time status printed per company
- `projects/form-fill/log.csv` — full audit log of every attempt
- `projects/form-fill/learnings.json` — success/failure patterns, improves over runs
- Final summary: submitted / email-only / failed / no-contact-found

## Message Sent

> Hey [Company Name],
>
> I saw you're hiring for a [role]. Before you bring someone on, I'd love to show you how
> our AI system handles all of that work — calls, scheduling, admin, follow-ups — for a
> fraction of the cost. Available 24/7, zero training time.
>
> Worth a quick look: silentaipartner.com
>
> — Wes
> CEO, Omnia Intelligence AI

## Dependencies

Install once:
```bash
pip install -r requirements.txt
playwright install chromium
```

## Contact Info Setup

Add to `CLAUDE.local.md`:
```
FORM_FILL_EMAIL=your@email.com
FORM_FILL_PHONE=your-phone
TWO_CAPTCHA_API_KEY=your-key
```

## Notes

- CAPTCHA handling via 2Captcha API (TWO_CAPTCHA_API_KEY in CLAUDE.local.md)
- Email-only results logged for manual follow-up
- Learns from each run — blocked domains and failure patterns are skipped next time
- Never runs autonomously — always invoked by Wes
