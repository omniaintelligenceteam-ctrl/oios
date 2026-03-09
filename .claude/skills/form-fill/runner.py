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
    contact_method = "none"

    try:
        site_url = listing.company_website or f"https://www.google.com/search?q={listing.company_name.replace(' ', '+')}+contact"
        contact = await find_contact(page, site_url)

        if contact.has_form:
            await page.goto(contact.form_url, wait_until="domcontentloaded", timeout=15000)
            submitted = await fill_form(page, listing.company_name, listing.job_title, CAPTCHA_API_KEY)
            status = "submitted" if submitted else "failed"
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
        site_url=listing.company_website or "",
        contact_method=contact_method,
        job_title=listing.job_title,
        status=status
    )

    return status

async def run(query: str, limit: int, parallel: int):
    print(f"\n[form-fill] Starting: query='{query}' limit={limit} parallel={parallel}\n")

    # Load learnings to skip known-bad domains
    from learner import load_learnings
    learnings = load_learnings()
    if learnings['blocked_domains']:
        print(f"[learner] Skipping {len(learnings['blocked_domains'])} known-blocked domains")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        scrape_page = await browser.new_page()
        listings = await scrape_indeed(scrape_page, query, limit)
        await scrape_page.close()

        print(f"[form-fill] Found {len(listings)} companies. Processing...\n")

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

    # Update learnings after every run
    from learner import update_learnings
    update_learnings(LOG_FILE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Job search query (e.g. "receptionist hiring")')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--parallel', type=int, default=5)
    args = parser.parse_args()
    asyncio.run(run(args.query, args.limit, args.parallel))
