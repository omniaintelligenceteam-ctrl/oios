# form_filler.py
import re
import os
from typing import Optional, Tuple, Dict
from bs4 import BeautifulSoup

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
    'email':   os.environ.get('FORM_FILL_EMAIL', 'wes@omniaintelligence.ai'),
    'phone':   os.environ.get('FORM_FILL_PHONE', ''),
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

    captcha_type, site_key = detect_captcha_type(html)
    if captcha_type and site_key and captcha_api_key:
        if captcha_type == 'recaptcha':
            token = solve_recaptcha(site_key, page.url, captcha_api_key)
        else:
            token = solve_hcaptcha(site_key, page.url, captcha_api_key)
        await page.evaluate(f'document.getElementById("g-recaptcha-response").value = "{token}"')

    submit_btn = await page.query_selector('button[type="submit"], input[type="submit"]')
    if submit_btn:
        await submit_btn.click()
        await page.wait_for_timeout(2000)
        return True

    return False
