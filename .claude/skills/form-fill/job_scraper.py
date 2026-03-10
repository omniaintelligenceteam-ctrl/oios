# job_scraper.py
from dataclasses import dataclass, field
from typing import List
from bs4 import BeautifulSoup

# Skip large enterprise companies — not OIOS targets
ENTERPRISE_KEYWORDS = [
    'hospital', 'health system', 'medical center', 'senior living', 'senior care',
    'healthcare', 'urgent care', 'clinic', 'university', 'college', 'school district',
    'government', 'federal', 'county', 'city of', 'department of',
    'staffing', 'temp agency', 'recruiter', 'indeed', 'ziprecruiter',
    'walmart', 'amazon', 'target', 'costco', 'kroger', 'cvs', 'walgreens',
]

# Skip placeholder/anonymous company names
SKIP_NAMES = {'confidential', 'anonymous', 'undisclosed', 'private company', 'carrier'}

def is_service_business(company_name: str) -> bool:
    name_lower = company_name.lower().strip()
    if name_lower in SKIP_NAMES:
        return False
    return not any(kw in name_lower for kw in ENTERPRISE_KEYWORDS)

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
        company = card.select_one('[data-testid="company-name"]')
        title = card.select_one('span[id^="jobTitle-"]')
        if company and title:
            name = company.get_text(strip=True)
            if is_service_business(name):
                listings.append(JobListing(
                    company_name=name,
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
