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
python runner.py "<query>"
```

**Always dry-run first to preview what will be sent:**
```bash
python runner.py "receptionist hiring" --limit 10 --dry-run
```

**Then run live when you're happy with it:**
```bash
python runner.py "receptionist hiring" --limit 10
python runner.py "plumbing office manager" --limit 20
python runner.py "HVAC admin assistant" --limit 20 --parallel 2
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| query | required | Job title to search for |
| --limit | 20 | Max companies to process |
| --parallel | 1 | Simultaneous browser agents (keep at 1 for accuracy) |
| --dry-run | off | Find forms but do NOT submit — preview only |
| --headless | off | Run browser invisibly |

**Deduplication is automatic** — already-contacted companies are skipped every run.

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
