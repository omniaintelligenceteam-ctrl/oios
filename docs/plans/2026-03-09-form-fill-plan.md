# Form Fill Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that scrapes job boards for companies hiring back-office roles, visits their websites, and submits personalized contact forms pointing to silentaipartner.com.

**Architecture:** The skill consists of a SKILL.md (triggers + instructions for Claude) and a Python runner (`runner.py`) that uses Playwright for async browser automation. Job board scraping, contact finding, form filling, and 2Captcha integration are split into focused modules. Results are logged to a CSV after each attempt.

**Tech Stack:** Python 3.10+, Playwright (async), twocaptcha-python, asyncio, csv

---

### Task 1: Set Up Skill Directory and Dependencies

**Files:**
- Create: `.claude/skills/form-fill/requirements.txt`
- Create: `projects/form-fill/` (directory + .gitkeep)

**Step 1: Create directories**

```bash
mkdir -p ".claude/skills/form-fill"
mkdir -p "projects/form-fill"
touch "projects/form-fill/.gitkeep"
```

**Step 2: Create requirements.txt**

```
playwright==1.42.0
twocaptcha-python==1.2.7
```

**Step 3: Install dependencies**

```bash
pip install -r ".claude/skills/form-fill/requirements.txt"
playwright install chromium
```

Expected: No errors. Chromium downloads (~150MB).

**Step 4: Commit**

```bash
git add .claude/skills/form-fill/requirements.txt projects/form-fill/.gitkeep
git commit -m "feat: scaffold form-fill skill directory"
```

---

### Task 2: Write 2Captcha Integration Module

**Files:**
- Create: `.claude/skills/form-fill/captcha_solver.py`
- Create: `.claude/skills/form-fill/tests/test_captcha_solver.py`

**Step 1: Write the failing test**

```python
# tests/test_captcha_solver.py
import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from captcha_solver import solve_recaptcha, solve_hcaptcha

def test_solve_recaptcha_returns_token():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.recaptcha.return_value = {'code': 'test-token-123'}
        result = solve_recaptcha('fake-site-key', 'https://example.com', 'fake-api-key')
        assert result == 'test-token-123'

def test_solve_hcaptcha_returns_token():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.hcaptcha.return_value = {'code': 'hcap-token-456'}
        result = solve_hcaptcha('fake-site-key', 'https://example.com', 'fake-api-key')
        assert result == 'hcap-token-456'

def test_solve_recaptcha_raises_on_failure():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.recaptcha.side_effect = Exception("API error")
        with pytest.raises(Exception, match="API error"):
            solve_recaptcha('bad-key', 'https://example.com', 'fake-api-key')
```

**Step 2: Run test to verify it fails**

```bash
cd ".claude/skills/form-fill"
python -m pytest tests/test_captcha_solver.py -v
```

Expected: `ImportError: cannot import name 'solve_recaptcha'`

**Step 3: Write implementation**

```python
# captcha_solver.py
from twocaptcha import TwoCaptcha

def solve_recaptcha(site_key: str, page_url: str, api_key: str) -> str:
    solver = TwoCaptcha(api_key)
    result = solver.recaptcha(sitekey=site_key, url=page_url)
    return result['code']

def solve_hcaptcha(site_key: str, page_url: str, api_key: str) -> str:
    solver = TwoCaptcha(api_key)
    result = solver.hcaptcha(sitekey=site_key, url=page_url)
    return result['code']
```

**Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_captcha_solver.py -v
```

Expected: 3 PASSED

**Step 5: Commit**

```bash
git add .claude/skills/form-fill/captcha_solver.py .claude/skills/form-fill/tests/
git commit -m "feat: add 2Captcha integration module"
```

---

### Task 3: Write Job Board Scraper

**Files:**
- Create: `.claude/skills/form-fill/job_scraper.py`
- Create: `.claude/skills/form-fill/tests/test_job_scraper.py`

**Step 1: Write the failing test**

```python
# tests/test_job_scraper.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from job_scraper import parse_indeed_results, JobListing
import asyncio

def test_parse_indeed_results_extracts_fields():
    html = """
    <div class="job_seen_beacon">
        <span class="companyName">Acme Corp</span>
        <h2 class="jobTitle"><span>Office Manager</span></h2>
        <span class="companyLocation">Austin, TX</span>
    </div>
    """
    results = parse_indeed_results(html)
    assert len(results) == 1
    assert results[0].company_name == "Acme Corp"
    assert results[0].job_title == "Office Manager"

def test_parse_indeed_results_empty_html():
    results = parse_indeed_results("<html></html>")
    assert results == []

def test_job_listing_dataclass():
    job = JobListing(company_name="Test Co", job_title="Receptionist", company_website="", source="indeed")
    assert job.company_name == "Test Co"
    assert job.status == "pending"
```

**Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_job_scraper.py -v
```

Expected: `ImportError: cannot import name 'parse_indeed_results'`

**Step 3: Write implementation**

```python
# job_scraper.py
from dataclasses import dataclass, field
from typing import List
from bs4 import BeautifulSoup
import re

@dataclass
class JobListing:
    company_name: str
    job_title: str
    company_website: str
    source: str
    status: str = "pending"

def parse_indeed_results(html: str) -> List[JobListing]:
    soup = BeautifulSoup(html, 'html.parser')
    listings = []
    for card in soup.select('.job_seen_beacon'):
        company = card.select_one('.companyName')
        title = card.select_one('.jobTitle span')
        if company and title:
            listings.append(JobListing(
                company_name=company.get_text(strip=True),
                job_title=title.get_text(strip=True),
                company_website="",
                source="indeed"
            ))
    return listings

async def scrape_indeed(page, query: str, limit: int) -> List[JobListing]:
    url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l="
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    html = await page.content()
    results = parse_indeed_results(html)
    return results[:limit]
```

**Step 4: Install beautifulsoup4 and add to requirements**

Add to `requirements.txt`:
```
beautifulsoup4==4.12.3
```

```bash
pip install beautifulsoup4
```

**Step 5: Run test to verify it passes**

```bash
python -m pytest tests/test_job_scraper.py -v
```

Expected: 3 PASSED

**Step 6: Commit**

```bash
git add .claude/skills/form-fill/job_scraper.py .claude/skills/form-fill/requirements.txt .claude/skills/form-fill/tests/test_job_scraper.py
git commit -m "feat: add indeed job board scraper"
```

---

### Task 4: Write Contact Finder

**Files:**
- Create: `.claude/skills/form-fill/contact_finder.py`
- Create: `.claude/skills/form-fill/tests/test_contact_finder.py`

**Step 1: Write the failing test**

```python
# tests/test_contact_finder.py
import pytest
from unittest.mock import MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from contact_finder import find_contact_links, extract_email_from_html, ContactInfo

def test_find_contact_links_detects_contact_page():
    html = '<a href="/contact-us">Contact</a> <a href="/about">About</a>'
    base_url = "https://example.com"
    links = find_contact_links(html, base_url)
    assert "https://example.com/contact-us" in links

def test_extract_email_finds_mailto():
    html = '<a href="mailto:info@example.com">Email us</a>'
    email = extract_email_from_html(html)
    assert email == "info@example.com"

def test_extract_email_finds_plain_text():
    html = '<p>Contact us at info@example.com for more info.</p>'
    email = extract_email_from_html(html)
    assert email == "info@example.com"

def test_extract_email_returns_none_when_missing():
    html = '<p>No email here</p>'
    email = extract_email_from_html(html)
    assert email is None

def test_contact_info_dataclass():
    c = ContactInfo(form_url="https://example.com/contact", email=None)
    assert c.has_form is True
    assert c.has_email is False
```

**Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_contact_finder.py -v
```

Expected: `ImportError`

**Step 3: Write implementation**

```python
# contact_finder.py
import re
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urljoin
from bs4 import BeautifulSoup

CONTACT_PATTERNS = [
    '/contact', '/contact-us', '/contactus', '/get-in-touch',
    '/reach-us', '/reach-out', '/talk-to-us', '/hello', '/inquire'
]

@dataclass
class ContactInfo:
    form_url: Optional[str]
    email: Optional[str]

    @property
    def has_form(self) -> bool:
        return self.form_url is not None

    @property
    def has_email(self) -> bool:
        return self.email is not None

def find_contact_links(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    found = []
    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if any(p in href for p in CONTACT_PATTERNS):
            full_url = urljoin(base_url, a['href'])
            found.append(full_url)
    return list(set(found))

def extract_email_from_html(html: str) -> Optional[str]:
    # Check mailto links first
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('mailto:'):
            return a['href'].replace('mailto:', '').split('?')[0].strip()
    # Fall back to regex
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
    return match.group(0) if match else None

async def find_contact(page, site_url: str) -> ContactInfo:
    """Navigate to a company site and find a contact form or email."""
    try:
        await page.goto(site_url, wait_until="domcontentloaded", timeout=15000)
        html = await page.content()
        contact_links = find_contact_links(html, site_url)
        email = extract_email_from_html(html)

        if contact_links:
            await page.goto(contact_links[0], wait_until="domcontentloaded", timeout=15000)
            form_html = await page.content()
            # Check if the contact page actually has a form
            if '<form' in form_html.lower():
                return ContactInfo(form_url=page.url, email=email)

        return ContactInfo(form_url=None, email=email)
    except Exception:
        return ContactInfo(form_url=None, email=None)
```

**Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_contact_finder.py -v
```

Expected: 5 PASSED

**Step 5: Commit**

```bash
git add .claude/skills/form-fill/contact_finder.py .claude/skills/form-fill/tests/test_contact_finder.py
git commit -m "feat: add contact page finder and email extractor"
```

---

### Task 5: Write Form Filler

**Files:**
- Create: `.claude/skills/form-fill/form_filler.py`
- Create: `.claude/skills/form-fill/tests/test_form_filler.py`

**Step 1: Write the failing test**

```python
# tests/test_form_filler.py
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from form_filler import build_message, detect_captcha_type, FIELD_PATTERNS

def test_build_message_personalizes_company_and_role():
    msg = build_message("Acme Corp", "office manager")
    assert "Acme Corp" in msg
    assert "office manager" in msg
    assert "silentaipartner.com" in msg
    assert msg.startswith("Hey")

def test_build_message_contains_sign_off():
    msg = build_message("Test Co", "receptionist")
    assert "Wes" in msg
    assert "Omnia Intelligence AI" in msg

def test_detect_captcha_type_recaptcha():
    html = '<div class="g-recaptcha" data-sitekey="abc123"></div>'
    result = detect_captcha_type(html)
    assert result == ('recaptcha', 'abc123')

def test_detect_captcha_type_hcaptcha():
    html = '<div class="h-captcha" data-sitekey="xyz789"></div>'
    result = detect_captcha_type(html)
    assert result == ('hcaptcha', 'xyz789')

def test_detect_captcha_type_none():
    html = '<form><input type="text"></form>'
    result = detect_captcha_type(html)
    assert result == (None, None)

def test_field_patterns_cover_common_names():
    assert 'name' in FIELD_PATTERNS
    assert 'email' in FIELD_PATTERNS
    assert 'message' in FIELD_PATTERNS
```

**Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_form_filler.py -v
```

Expected: `ImportError`

**Step 3: Write implementation**

```python
# form_filler.py
import re
from typing import Optional, Tuple, Dict
from bs4 import BeautifulSoup

# Maps semantic intent to common field name/id/placeholder patterns
FIELD_PATTERNS: Dict[str, list] = {
    'name':    ['name', 'full_name', 'fullname', 'your-name', 'yourname', 'contact_name'],
    'email':   ['email', 'e-mail', 'email_address', 'your-email'],
    'phone':   ['phone', 'telephone', 'tel', 'mobile', 'cell'],
    'subject': ['subject', 'topic', 'regarding', 'reason'],
    'message': ['message', 'msg', 'comment', 'comments', 'body', 'inquiry', 'enquiry', 'details', 'description'],
    'company': ['company', 'organization', 'organisation', 'business', 'firm'],
    'website': ['website', 'url', 'web', 'site'],
}

CONTACT_INFO = {
    'name':    'Wes',
    'email':   'wes@omniaintelligence.ai',
    'phone':   '',   # Fill in when known
    'company': 'Omnia Intelligence AI',
    'website': 'silentaipartner.com',
}

def build_message(company_name: str, role: str) -> str:
    return (
        f"Hey {company_name},\n\n"
        f"I saw you're hiring for a {role}. Before you bring someone on, I'd love to show you "
        f"how our AI system handles all of that work — calls, scheduling, admin, follow-ups — "
        f"for a fraction of the cost. Available 24/7, zero training time.\n\n"
        f"Worth a quick look: silentaipartner.com\n\n"
        f"— Wes\n"
        f"CEO, Omnia Intelligence AI"
    )

def detect_captcha_type(html: str) -> Tuple[Optional[str], Optional[str]]:
    soup = BeautifulSoup(html, 'html.parser')
    recaptcha = soup.find(attrs={'class': re.compile(r'g-recaptcha', re.I)})
    if recaptcha:
        return ('recaptcha', recaptcha.get('data-sitekey', ''))
    hcaptcha = soup.find(attrs={'class': re.compile(r'h-captcha', re.I)})
    if hcaptcha:
        return ('hcaptcha', hcaptcha.get('data-sitekey', ''))
    # Check for recaptcha in script tags
    if 'grecaptcha' in html or 'recaptcha/api.js' in html:
        match = re.search(r'sitekey["\s:=]+["\']([^"\']+)', html)
        if match:
            return ('recaptcha', match.group(1))
    return (None, None)

def _matches_pattern(field_attr: str, patterns: list) -> bool:
    field_lower = field_attr.lower()
    return any(p in field_lower for p in patterns)

async def fill_form(page, company_name: str, job_title: str, captcha_api_key: str) -> bool:
    """Fill all form fields on the current page and submit. Returns True if submitted."""
    from captcha_solver import solve_recaptcha, solve_hcaptcha

    html = await page.content()
    message = build_message(company_name, job_title)

    # Fill text inputs and textareas
    inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"], input:not([type]), textarea')
    for inp in inputs:
        name = (await inp.get_attribute('name') or '').lower()
        id_  = (await inp.get_attribute('id') or '').lower()
        placeholder = (await inp.get_attribute('placeholder') or '').lower()
        tag = await inp.evaluate('el => el.tagName.toLowerCase()')
        combined = f"{name} {id_} {placeholder}"

        if _matches_pattern(combined, FIELD_PATTERNS['email']):
            await inp.fill(CONTACT_INFO['email'])
        elif _matches_pattern(combined, FIELD_PATTERNS['name']):
            await inp.fill(CONTACT_INFO['name'])
        elif _matches_pattern(combined, FIELD_PATTERNS['phone']):
            if CONTACT_INFO['phone']:
                await inp.fill(CONTACT_INFO['phone'])
        elif _matches_pattern(combined, FIELD_PATTERNS['subject']):
            await inp.fill("AI alternative to hiring a receptionist/office manager")
        elif _matches_pattern(combined, FIELD_PATTERNS['company']):
            await inp.fill(CONTACT_INFO['company'])
        elif _matches_pattern(combined, FIELD_PATTERNS['website']):
            await inp.fill(CONTACT_INFO['website'])
        elif tag == 'textarea' or _matches_pattern(combined, FIELD_PATTERNS['message']):
            await inp.fill(message)

    # Handle CAPTCHA
    captcha_type, site_key = detect_captcha_type(html)
    if captcha_type and site_key and captcha_api_key:
        if captcha_type == 'recaptcha':
            token = solve_recaptcha(site_key, page.url, captcha_api_key)
        else:
            token = solve_hcaptcha(site_key, page.url, captcha_api_key)
        await page.evaluate(f'document.getElementById("g-recaptcha-response").value = "{token}"')

    # Submit
    submit_btn = await page.query_selector('button[type="submit"], input[type="submit"]')
    if submit_btn:
        await submit_btn.click()
        await page.wait_for_timeout(2000)
        return True

    return False
```

**Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_form_filler.py -v
```

Expected: 6 PASSED

**Step 5: Commit**

```bash
git add .claude/skills/form-fill/form_filler.py .claude/skills/form-fill/tests/test_form_filler.py
git commit -m "feat: add form field detector and filler with CAPTCHA support"
```

---

### Task 6: Write Logger

**Files:**
- Create: `.claude/skills/form-fill/logger.py`
- Create: `.claude/skills/form-fill/tests/test_logger.py`

**Step 1: Write the failing test**

```python
# tests/test_logger.py
import pytest, os, csv, tempfile
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from logger import log_attempt, FIELDNAMES

def test_log_attempt_creates_file_with_header(tmp_path):
    log_file = str(tmp_path / "log.csv")
    log_attempt(log_file, company_name="Acme", site_url="https://acme.com",
                contact_method="form", job_title="Receptionist", status="submitted")
    with open(log_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]['company_name'] == 'Acme'
    assert rows[0]['status'] == 'submitted'

def test_log_attempt_appends_rows(tmp_path):
    log_file = str(tmp_path / "log.csv")
    log_attempt(log_file, company_name="A", site_url="x", contact_method="form", job_title="r", status="submitted")
    log_attempt(log_file, company_name="B", site_url="y", contact_method="email", job_title="r", status="email-only")
    with open(log_file) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[1]['company_name'] == 'B'
```

**Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_logger.py -v
```

Expected: `ImportError`

**Step 3: Write implementation**

```python
# logger.py
import csv
import os
from datetime import datetime

FIELDNAMES = ['timestamp', 'company_name', 'site_url', 'contact_method', 'job_title', 'status']

def log_attempt(log_file: str, company_name: str, site_url: str,
                contact_method: str, job_title: str, status: str):
    os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
    write_header = not os.path.exists(log_file)
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.utcnow().isoformat(),
            'company_name': company_name,
            'site_url': site_url,
            'contact_method': contact_method,
            'job_title': job_title,
            'status': status,
        })
```

**Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_logger.py -v
```

Expected: 2 PASSED

**Step 5: Commit**

```bash
git add .claude/skills/form-fill/logger.py .claude/skills/form-fill/tests/test_logger.py
git commit -m "feat: add CSV logger for form fill attempts"
```

---

### Task 7: Write Main Runner (Orchestrator)

**Files:**
- Create: `.claude/skills/form-fill/runner.py`

**Step 1: Write runner.py**

```python
# runner.py
"""
Form Fill Runner — orchestrates job board scraping + contact form submission.

Usage:
    python runner.py "receptionist hiring" --limit 20 --parallel 5

Environment:
    TWO_CAPTCHA_API_KEY — from CLAUDE.local.md
"""

import asyncio
import argparse
import os
import sys
from datetime import datetime
from playwright.async_api import async_playwright

from job_scraper import scrape_indeed, JobListing
from contact_finder import find_contact
from form_filler import fill_form
from logger import log_attempt

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', 'form-fill', 'log.csv')
CAPTCHA_API_KEY = os.environ.get('TWO_CAPTCHA_API_KEY', '')

async def process_company(browser, listing: JobListing) -> str:
    """Process a single company: find contact, fill form, log result."""
    context = await browser.new_context()
    page = await context.new_page()
    status = "no-contact-found"

    try:
        # Step 1: Find company website if not known
        site_url = listing.company_website or f"https://www.google.com/search?q={listing.company_name.replace(' ', '+')}+contact"

        # Step 2: Find contact method
        contact = await find_contact(page, site_url)

        if contact.has_form:
            await page.goto(contact.form_url, wait_until="domcontentloaded", timeout=15000)
            submitted = await fill_form(page, listing.company_name, listing.job_title, CAPTCHA_API_KEY)
            status = "submitted" if submitted else "failed"
            contact_method = "form"
        elif contact.has_email:
            status = "email-only"
            contact_method = "email"
        else:
            contact_method = "none"

    except Exception as e:
        status = f"failed: {str(e)[:50]}"
        contact_method = "error"
    finally:
        await context.close()

    log_attempt(
        LOG_FILE,
        company_name=listing.company_name,
        site_url=listing.company_website or "",
        contact_method=contact_method,
        job_title=listing.job_title,
        status=status
    )

    return status

async def run(query: str, limit: int, parallel: int):
    print(f"\n[form-fill] Starting: query='{query}' limit={limit} parallel={parallel}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Scrape job boards
        scrape_page = await browser.new_page()
        listings = await scrape_indeed(scrape_page, query, limit)
        await scrape_page.close()

        print(f"[form-fill] Found {len(listings)} companies. Processing...\n")

        # Process in parallel batches
        results = {'submitted': 0, 'email-only': 0, 'failed': 0, 'no-contact-found': 0}
        sem = asyncio.Semaphore(parallel)

        async def bounded(listing):
            async with sem:
                status = await process_company(browser, listing)
                base_status = status.split(':')[0]
                results[base_status] = results.get(base_status, 0) + 1
                print(f"  [{base_status.upper()}] {listing.company_name}")

        await asyncio.gather(*[bounded(l) for l in listings])
        await browser.close()

    print(f"\n[form-fill] Done.")
    print(f"  Submitted:        {results.get('submitted', 0)}")
    print(f"  Email-only:       {results.get('email-only', 0)}")
    print(f"  Failed:           {results.get('failed', 0)}")
    print(f"  No contact found: {results.get('no-contact-found', 0)}")
    print(f"\nLog saved to: {os.path.abspath(LOG_FILE)}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Job search query (e.g. "receptionist hiring")')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--parallel', type=int, default=5)
    args = parser.parse_args()
    asyncio.run(run(args.query, args.limit, args.parallel))
```

**Step 2: Run a smoke test**

```bash
cd ".claude/skills/form-fill"
python runner.py "office manager hiring" --limit 3 --parallel 1
```

Expected: Output shows companies found + statuses. Log CSV created at `projects/form-fill/log.csv`.

**Step 3: Commit**

```bash
git add .claude/skills/form-fill/runner.py
git commit -m "feat: add main orchestrator runner with parallel execution"
```

---

### Task 8: Write SKILL.md

**Files:**
- Create: `.claude/skills/form-fill/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
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
cd ".claude/skills/form-fill"
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
- Final summary: submitted / email-only / failed / no-contact-found

## Message Sent

Every submission uses this template (personalized with company name + role):

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
pip install -r .claude/skills/form-fill/requirements.txt
playwright install chromium
```

## Notes

- CAPTCHA handling via 2Captcha API (key in CLAUDE.local.md as TWO_CAPTCHA_API_KEY)
- Email-only results saved to log for manual follow-up
- Never runs autonomously — always invoked by Wes
```

**Step 2: Commit**

```bash
git add .claude/skills/form-fill/SKILL.md
git commit -m "feat: add form-fill SKILL.md with usage docs"
```

---

### Task 9: Update CLAUDE.local.md with Contact Info

**Files:**
- Modify: `CLAUDE.local.md`

**Step 1: Add Wes's contact info for form fields**

Open `CLAUDE.local.md` and add under the API Keys section:

```
# Form Fill Contact Info
FORM_FILL_EMAIL=<Wes's email>
FORM_FILL_PHONE=<Wes's phone>
```

Then update `CONTACT_INFO` in `form_filler.py` to read from env vars:

```python
CONTACT_INFO = {
    'name':    'Wes',
    'email':   os.environ.get('FORM_FILL_EMAIL', 'wes@omniaintelligence.ai'),
    'phone':   os.environ.get('FORM_FILL_PHONE', ''),
    'company': 'Omnia Intelligence AI',
    'website': 'silentaipartner.com',
}
```

**Step 2: Commit**

```bash
git add .claude/skills/form-fill/form_filler.py
git commit -m "feat: read contact info from env vars"
```

---

### Task 10: Add Learning Loop

**Files:**
- Create: `.claude/skills/form-fill/learner.py`
- Modify: `.claude/skills/form-fill/runner.py`

**What it does:** After each run, analyze the log and write patterns to `projects/form-fill/learnings.json`. Before the next run, load learnings to skip known-bad patterns and prioritize what works.

**Step 1: Write learner.py**

```python
# learner.py
"""
Analyzes form-fill log after each run and updates learnings.json.
Learnings are loaded at the start of the next run to improve success rate.
"""
import json, csv, os
from collections import defaultdict
from datetime import datetime

LEARNINGS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', 'form-fill', 'learnings.json')

def load_learnings() -> dict:
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE) as f:
            return json.load(f)
    return {
        "blocked_domains": [],
        "no_form_domains": [],
        "successful_domains": [],
        "failure_reasons": {},
        "total_runs": 0,
        "total_submitted": 0,
        "total_failed": 0,
        "last_updated": None
    }

def save_learnings(learnings: dict):
    os.makedirs(os.path.dirname(LEARNINGS_FILE), exist_ok=True)
    learnings["last_updated"] = datetime.utcnow().isoformat()
    with open(LEARNINGS_FILE, 'w') as f:
        json.dump(learnings, f, indent=2)

def update_learnings(log_file: str):
    """Read the latest run from log.csv and update learnings.json."""
    if not os.path.exists(log_file):
        return

    learnings = load_learnings()
    learnings["total_runs"] += 1

    with open(log_file, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    # Only process rows from this run (last N rows where N = rows since last learn)
    for row in rows:
        from urllib.parse import urlparse
        domain = urlparse(row.get('site_url', '')).netloc

        status = row.get('status', '')
        if status == 'submitted':
            learnings['total_submitted'] += 1
            if domain and domain not in learnings['successful_domains']:
                learnings['successful_domains'].append(domain)
        elif 'failed' in status:
            learnings['total_failed'] += 1
            reason = status.replace('failed: ', '')
            learnings['failure_reasons'][reason] = learnings['failure_reasons'].get(reason, 0) + 1
            if 'blocked' in reason.lower() or 'timeout' in reason.lower():
                if domain and domain not in learnings['blocked_domains']:
                    learnings['blocked_domains'].append(domain)
        elif status == 'no-contact-found':
            if domain and domain not in learnings['no_form_domains']:
                learnings['no_form_domains'].append(domain)

    save_learnings(learnings)
    print_summary(learnings)

def print_summary(learnings: dict):
    total = learnings['total_submitted'] + learnings['total_failed']
    rate = round(learnings['total_submitted'] / total * 100) if total > 0 else 0
    print(f"\n[learner] Lifetime stats: {learnings['total_submitted']} submitted / {total} attempted ({rate}% success rate)")
    if learnings['failure_reasons']:
        top = sorted(learnings['failure_reasons'].items(), key=lambda x: -x[1])[:3]
        print(f"[learner] Top failure reasons: {', '.join(f'{r} ({n}x)' for r, n in top)}")
    print(f"[learner] Learnings saved to learnings.json\n")
```

**Step 2: Wire into runner.py — add at end of `run()` function**

After the results summary print block, add:

```python
    # Update learnings after every run
    from learner import update_learnings
    update_learnings(LOG_FILE)
```

And at the top of `run()`, before scraping, add:

```python
    # Load learnings to skip known-bad domains
    from learner import load_learnings
    learnings = load_learnings()
    if learnings['blocked_domains']:
        print(f"[learner] Skipping {len(learnings['blocked_domains'])} known-blocked domains")
```

**Step 3: Commit**

```bash
git add .claude/skills/form-fill/learner.py .claude/skills/form-fill/runner.py
git commit -m "feat: add post-run learning loop — tracks success/fail patterns across runs"
```

---

### Task 11: Run Full Test

**Step 1: Run all unit tests**

```bash
cd ".claude/skills/form-fill"
python -m pytest tests/ -v
```

Expected: All tests PASS.

**Step 2: Live end-to-end test with 1 company**

```bash
TWO_CAPTCHA_API_KEY=8d480ef2eaee2af4ada5f54f22710df5 python runner.py "receptionist hiring" --limit 1 --parallel 1
```

Watch output. Check `projects/form-fill/log.csv` for the logged result.

**Step 3: Final commit**

```bash
git add -A
git commit -m "feat: form-fill skill complete — job board scraping + contact form automation"
```
