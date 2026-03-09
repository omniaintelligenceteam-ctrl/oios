# Form Fill Skill — Design Doc

**Date:** 2026-03-09
**Status:** Approved
**Skill path:** `.claude/skills/form-fill/SKILL.md`

---

## Problem

Companies actively hiring for receptionist, office manager, or back-office roles are the perfect OIOS targets — they're already signaling the pain we solve. This skill automates reaching out to them at scale via their website contact forms.

---

## Goal

Given a job search query, automatically:
1. Find companies on job boards that are hiring for back-office roles
2. Visit each company's website and locate their contact form or email
3. Fill and submit the form with personalized contact details + a message pointing to silentaipartner.com
4. Log every attempt for tracking

---

## Architecture

### Tech
- **Browser automation:** `multi-agent-chrome` skill (Chrome DevTools MCP)
- **CAPTCHA solving:** 2Captcha API (`TWO_CAPTCHA_API_KEY` in CLAUDE.local.md)
- **Parallelism:** Up to 5 Chrome agents running simultaneously
- **Logging:** `projects/form-fill/log.csv`

### Pipeline (5 phases)

1. **Discover** — Chrome agent(s) search job boards (Indeed, LinkedIn Jobs, ZipRecruiter) for the given query. Extract: company name, job title, company website URL.

2. **Find Contact** — For each company, navigate to their site. Locate contact page, form, or footer email. Priority: contact form > email.

3. **Fill & Submit** — Fill form fields with Wes's contact info + personalized message. Handle CAPTCHAs via 2Captcha. Submit.

4. **Fallback** — If no form is found but an email exists, log it as `email-only` for a follow-up manual or email-based outreach pass.

5. **Log Results** — Append to `projects/form-fill/log.csv`:
   - company_name, site_url, contact_method, job_title, status, timestamp
   - Status values: `submitted`, `failed`, `email-only`, `no-contact-found`

---

## Message Template

**Subject field (if present):**
> AI alternative to hiring a receptionist/office manager

**Body:**
> Hey [Company Name],
>
> I saw you're hiring for a [role]. Before you bring someone on, I'd love to show you how our AI system handles all of that work — calls, scheduling, admin, follow-ups — for a fraction of the cost. Available 24/7, zero training time.
>
> Worth a quick look: silentaipartner.com
>
> — Wes
> CEO, Omnia Intelligence AI

**Personalization variables:**
- `[Company Name]` — from job listing
- `[role]` — job title from listing (e.g. "receptionist", "office manager")

---

## Contact Info (fills form fields)

- **Name:** Wes
- **Email:** (Wes to provide)
- **Phone:** (Wes to provide)
- **Company:** Omnia Intelligence AI
- **Website:** silentaipartner.com

---

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | Job search term (e.g. "receptionist hiring") |
| `boards` | No | Indeed, LinkedIn, ZipRecruiter | Job boards to search |
| `limit` | No | 20 | Max companies to process per run |
| `parallel` | No | 5 | Number of simultaneous Chrome agents |

---

## Output

- Submissions fired to company contact forms
- `projects/form-fill/log.csv` updated after each attempt
- Summary printed at end: X submitted, X email-only, X failed

---

## CAPTCHA Integration

1. Chrome agent detects CAPTCHA on page
2. Sends to 2Captcha API with `TWO_CAPTCHA_API_KEY`
3. Polls for solution (10-30 sec average)
4. Injects token into form's hidden field
5. Proceeds with submission
6. Supports: reCAPTCHA v2/v3, hCaptcha, image challenges

---

## Constraints

- Never send without Wes's context — skill is invoked intentionally, no autonomous triggering
- Log all attempts regardless of outcome
- Respect per-site rate limits — don't hammer the same domain
- Keep message consistent — no hallucinating company-specific claims
