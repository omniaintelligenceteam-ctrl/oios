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
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('mailto:'):
            return a['href'].replace('mailto:', '').split('?')[0].strip()
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
            if '<form' in form_html.lower():
                return ContactInfo(form_url=page.url, email=email)

        return ContactInfo(form_url=None, email=email)
    except Exception:
        return ContactInfo(form_url=None, email=None)
