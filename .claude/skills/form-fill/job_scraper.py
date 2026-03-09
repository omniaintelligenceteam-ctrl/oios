# job_scraper.py
from dataclasses import dataclass, field
from typing import List
from bs4 import BeautifulSoup

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
