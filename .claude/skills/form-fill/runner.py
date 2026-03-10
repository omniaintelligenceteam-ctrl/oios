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
import csv
import os
from playwright.async_api import async_playwright

from job_scraper import scrape_indeed, JobListing
from contact_finder import find_contact
from form_filler import fill_form, build_message
from logger import log_attempt

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', 'form-fill', 'log.csv')

def _load_local_env():
    """Load env vars from CLAUDE.local.md if not already set."""
    local_md = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'CLAUDE.local.md')
    if not os.path.exists(local_md):
        return
    with open(local_md, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#') and not line.startswith('`'):
                key, _, val = line.partition('=')
                key = key.strip()
                val = val.strip().strip('`')
                if key and val and key not in os.environ:
                    os.environ[key] = val

def _load_contacted_companies() -> set:
    """Load company names already contacted (skip on next run)."""
    if not os.path.exists(LOG_FILE):
        return set()
    contacted = set()
    with open(LOG_FILE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            status = row.get('status', '')
            if status.startswith('submitted') or status == 'email-only':
                contacted.add(row.get('company_name', '').strip().lower())
    return contacted

_load_local_env()
CAPTCHA_API_KEY = os.environ.get('TWO_CAPTCHA_API_KEY', '')
if CAPTCHA_API_KEY:
    print(f"[captcha] 2Captcha key loaded ({CAPTCHA_API_KEY[:6]}...)")
else:
    print("[captcha] No 2Captcha key found — CAPTCHAs will be skipped")

async def process_company(browser, listing: JobListing, dry_run: bool = False) -> str:
    """Process a single company: find contact, fill form, log result."""
    context = await browser.new_context()
    page = await context.new_page()
    status = "no-contact-found"
    contact_method = "none"
    site_url = ""

    try:
        if listing.company_website:
            site_url = listing.company_website
        else:
            # DuckDuckGo HTML — no JS, no consent wall, bot-friendly
            import urllib.parse
            ddg_query = urllib.parse.quote(listing.company_name + ' official website')
            print(f"  [ddg] Searching: {listing.company_name}")
            await page.goto(f"https://html.duckduckgo.com/html/?q={ddg_query}", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(1000)
            # Skip ad results — only grab organic links
            first_result = await page.query_selector('.result:not(.result--ad) a.result__a')
            site_url = None
            if first_result:
                href = await first_result.get_attribute('href') or ''
                if 'uddg=' in href:
                    site_url = urllib.parse.unquote(href.split('uddg=')[1].split('&')[0])
                elif href.startswith('http'):
                    site_url = href
            print(f"  [ddg] Found URL: {site_url}")

        if not site_url:
            print(f"  [skip] No URL found for {listing.company_name}")
            contact = type('C', (), {'has_form': False, 'has_email': False})()
        else:
            print(f"  [contact] Scanning: {site_url}")
            contact = await find_contact(page, site_url)
            print(f"  [contact] has_form={contact.has_form} has_email={contact.has_email} form_url={getattr(contact, 'form_url', None)} email={getattr(contact, 'email', None)}")

        if contact.has_form:
            await page.goto(contact.form_url, wait_until="domcontentloaded", timeout=15000)
            if dry_run:
                msg = build_message(listing.company_name, listing.job_title)
                print(f"  [DRY-RUN] Would submit to: {contact.form_url}")
                print(f"  [DRY-RUN] Message: {msg[:120].strip()}...")
                status = "dry-run"
                contact_method = "form"
            else:
                submitted = await fill_form(page, listing.company_name, listing.job_title, CAPTCHA_API_KEY)
                status = "submitted" if submitted else "submitted-unconfirmed"
                contact_method = "form"
        elif contact.has_email:
            status = "email-only"
            contact_method = "email"

    except Exception as e:
        status = f"failed: {str(e)[:50]}"
        contact_method = "error"
    finally:
        await context.close()

    log_attempt(
        LOG_FILE,
        company_name=listing.company_name,
        site_url=site_url or "",
        contact_method=contact_method,
        job_title=listing.job_title,
        status=status
    )

    return status

async def process_company_manual(browser, listing: JobListing):
    """Find and fill a form without submitting. Returns (context, site_url, status) — context stays open."""
    context = await browser.new_context()
    page = await context.new_page()
    site_url = ""
    status = "no-contact-found"

    try:
        if listing.company_website:
            site_url = listing.company_website
        else:
            import urllib.parse
            ddg_query = urllib.parse.quote(listing.company_name + ' official website')
            print(f"  [ddg] Searching: {listing.company_name}")
            await page.goto(f"https://html.duckduckgo.com/html/?q={ddg_query}", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(1000)
            first_result = await page.query_selector('.result:not(.result--ad) a.result__a')
            if first_result:
                href = await first_result.get_attribute('href') or ''
                if 'uddg=' in href:
                    site_url = urllib.parse.unquote(href.split('uddg=')[1].split('&')[0])
                elif href.startswith('http'):
                    site_url = href
            print(f"  [ddg] Found URL: {site_url}")

        if not site_url:
            await context.close()
            return None, site_url, "no-contact-found"

        contact = await find_contact(page, site_url)
        if contact.has_form:
            await page.goto(contact.form_url, wait_until="domcontentloaded", timeout=15000)
            await fill_form(page, listing.company_name, listing.job_title, CAPTCHA_API_KEY, submit=False)
            print(f"  [READY] {listing.company_name} → {contact.form_url}")
            status = "manual-review"
        else:
            await context.close()
            return None, site_url, "no-contact-found"

    except Exception as e:
        await context.close()
        return None, site_url, f"failed: {str(e)[:50]}"

    # Return context open so user can submit
    return context, site_url, status

async def run(query: str, limit: int, parallel: int, headless: bool = False, dry_run: bool = False, manual: bool = False):
    if manual:
        mode = "MANUAL"
    elif dry_run:
        mode = "DRY-RUN"
    else:
        mode = "LIVE"
    print(f"\n[form-fill] Starting: query='{query}' limit={limit} mode={mode}\n")

    # Load learnings to skip known-bad domains
    from learner import load_learnings
    learnings = load_learnings()
    if learnings['blocked_domains']:
        print(f"[learner] Skipping {len(learnings['blocked_domains'])} known-blocked domains")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)

        scrape_page = await browser.new_page()
        listings = await scrape_indeed(scrape_page, query, limit)
        await scrape_page.close()

        # Deduplicate — skip companies already contacted
        contacted = _load_contacted_companies()
        before = len(listings)
        listings = [l for l in listings if l.company_name.strip().lower() not in contacted]
        skipped = before - len(listings)
        if skipped:
            print(f"[dedup] Skipping {skipped} already-contacted companies")

        print(f"[form-fill] Found {len(listings)} new companies. Processing...\n")

        results = {'submitted': 0, 'email-only': 0, 'failed': 0, 'no-contact-found': 0, 'dry-run': 0, 'manual-review': 0}

        if manual:
            # Manual mode: open 4 at a time, fill forms, wait for user to submit, then close and continue
            batch_size = 4
            loop = asyncio.get_event_loop()
            for i in range(0, len(listings), batch_size):
                batch = listings[i:i+batch_size]
                print(f"\n[manual] Batch {i//batch_size + 1}: opening {len(batch)} forms...\n")
                open_contexts = []
                for listing in batch:
                    ctx, site_url, status = await process_company_manual(browser, listing)
                    if ctx:
                        open_contexts.append((ctx, listing, site_url, status))
                        results['manual-review'] = results.get('manual-review', 0) + 1
                    else:
                        results[status.split(':')[0]] = results.get(status.split(':')[0], 0) + 1
                        log_attempt(LOG_FILE, company_name=listing.company_name, site_url=site_url or "",
                                    contact_method="none", job_title=listing.job_title, status=status)

                if open_contexts:
                    print(f"\n{'='*60}")
                    print(f"  {len(open_contexts)} browser(s) are open with forms filled.")
                    print(f"  Review, adjust the message, and click Send in each window.")
                    print(f"  Then come back here and press Enter to continue.")
                    print(f"{'='*60}\n")
                    await loop.run_in_executor(None, input, "Press Enter when done with this batch... ")
                    for ctx, listing, site_url, status in open_contexts:
                        log_attempt(LOG_FILE, company_name=listing.company_name, site_url=site_url or "",
                                    contact_method="form", job_title=listing.job_title, status="manual-review")
                        await ctx.close()
        else:
            sem = asyncio.Semaphore(parallel)

            async def bounded(listing):
                async with sem:
                    status = await process_company(browser, listing, dry_run=dry_run)
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

    # Update learnings after every run
    from learner import update_learnings
    update_learnings(LOG_FILE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Job search query (e.g. "receptionist hiring")')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--parallel', type=int, default=1)
    parser.add_argument('--headless', action='store_true', default=False, help='Run browser invisibly')
    parser.add_argument('--dry-run', action='store_true', default=False, help='Find forms but do not submit — preview only')
    parser.add_argument('--manual', action='store_true', default=False, help='Open pre-filled forms in browser for manual review and submission')
    args = parser.parse_args()
    asyncio.run(run(args.query, args.limit, args.parallel, args.headless, args.dry_run, args.manual))
