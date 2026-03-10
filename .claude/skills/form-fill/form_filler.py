# form_filler.py
import re
import os
from typing import Optional, Tuple, Dict
from bs4 import BeautifulSoup

FIELD_PATTERNS: Dict[str, list] = {
    'first_name': ['first_name', 'firstname', 'first-name', 'fname', 'given_name'],
    'last_name':  ['last_name', 'lastname', 'last-name', 'lname', 'surname', 'family_name'],
    'name':    ['name', 'full_name', 'fullname', 'your-name', 'yourname', 'contact_name'],
    'email':   ['email', 'e-mail', 'email_address', 'your-email'],
    'phone':   ['phone', 'telephone', 'tel', 'mobile', 'cell'],
    'subject': ['subject', 'topic', 'regarding', 'reason'],
    'message': ['message', 'msg', 'comment', 'comments', 'body', 'inquiry', 'enquiry', 'details', 'description'],
    'company': ['company', 'organization', 'organisation', 'business', 'firm'],
    'website': ['website', 'url', 'web', 'site'],
}

def _get_contact_info() -> dict:
    """Read contact info fresh from env each call so runner's env loading takes effect."""
    first = os.environ.get('FORM_FILL_FIRST_NAME', 'Sarah')
    last  = os.environ.get('FORM_FILL_LAST_NAME', 'Mitchell')
    return {
        'first_name': first,
        'last_name':  last,
        'name':       f"{first} {last}",
        'email':      os.environ.get('FORM_FILL_EMAIL', 'team@silentaipartner.com'),
        'phone':      os.environ.get('FORM_FILL_PHONE', ''),
        'company':    'Omnia Intelligence AI',
        'website':    'silentaipartner.com',
    }

def build_message(company_name: str, role: str) -> str:
    return (
        "Hey,\n\n"
        "I saw you're hiring. Before you bring someone on, I'd love to show you how our AI system "
        "handles all of that work that as a office manager would — calls, data entry, smart upsells, "
        "scheduling, admin, follow-ups — for a fraction of the cost. Available 24/7, zero training time.\n\n"
        "Worth a quick look: www.silentaipartner.com\n\n"
        "— Sarah Mitchell\n"
        "Omnia Intelligence AI"
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

async def fill_form(page, company_name: str, job_title: str, captcha_api_key: str, submit: bool = True) -> bool:
    """Fill all form fields on the current page. If submit=True, also click submit and verify."""
    from captcha_solver import solve_recaptcha, solve_hcaptcha

    html = await page.content()
    CONTACT_INFO = _get_contact_info()
    message = build_message(company_name, job_title)

    inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"], input:not([type]), textarea')
    for inp in inputs:
        name = (await inp.get_attribute('name') or '').lower()
        id_  = (await inp.get_attribute('id') or '').lower()
        placeholder = (await inp.get_attribute('placeholder') or '').lower()
        tag = await inp.evaluate('el => el.tagName.toLowerCase()')
        combined = f"{name} {id_} {placeholder}"

        value = None
        if _matches_pattern(combined, FIELD_PATTERNS['email']):
            value = CONTACT_INFO['email']
        elif _matches_pattern(combined, FIELD_PATTERNS['first_name']):
            value = CONTACT_INFO['first_name']
        elif _matches_pattern(combined, FIELD_PATTERNS['last_name']):
            value = CONTACT_INFO['last_name']
        elif _matches_pattern(combined, FIELD_PATTERNS['name']):
            value = CONTACT_INFO['name']
        elif _matches_pattern(combined, FIELD_PATTERNS['phone']):
            value = CONTACT_INFO['phone'] if CONTACT_INFO['phone'] else None
        elif _matches_pattern(combined, FIELD_PATTERNS['subject']):
            value = "AI alternative to hiring a receptionist/office manager"
        elif _matches_pattern(combined, FIELD_PATTERNS['company']):
            value = CONTACT_INFO['company']
        elif _matches_pattern(combined, FIELD_PATTERNS['website']):
            value = CONTACT_INFO['website']
        elif tag == 'textarea' or _matches_pattern(combined, FIELD_PATTERNS['message']):
            value = message

        if value:
            try:
                await inp.fill(value, timeout=5000)
            except Exception:
                # Fallback: inject value via JS (works for non-interactable elements)
                try:
                    await inp.evaluate(f'el => {{ el.value = {repr(value)}; el.dispatchEvent(new Event("input", {{bubbles:true}})); el.dispatchEvent(new Event("change", {{bubbles:true}})); }}')
                except Exception:
                    pass

    captcha_type, site_key = detect_captcha_type(html)
    if captcha_type and site_key and captcha_api_key:
        if captcha_type == 'recaptcha':
            token = solve_recaptcha(site_key, page.url, captcha_api_key)
        else:
            token = solve_hcaptcha(site_key, page.url, captcha_api_key)
        await page.evaluate(f'document.getElementById("g-recaptcha-response").value = "{token}"')

    if not submit:
        return True  # Fields filled — caller handles submission

    # Try strict submit first, then any button inside a form
    submit_btn = await page.query_selector('button[type="submit"], input[type="submit"]')
    if not submit_btn:
        submit_btn = await page.query_selector('form button:not([type="button"]):not([type="reset"])')
    if not submit_btn:
        return False

    url_before = page.url
    await submit_btn.click()
    await page.wait_for_timeout(3000)

    # Verify submission actually went through
    url_after = page.url
    page_text = (await page.content()).lower()

    SUCCESS_SIGNALS = [
        'thank you', 'thanks for', 'message sent', 'message received',
        'we received', "we'll be in touch", 'we will be in touch',
        'successfully submitted', 'form submitted', 'submission received',
        'we will contact', 'will get back', 'confirmation',
    ]

    url_changed = url_after != url_before
    success_text = any(s in page_text for s in SUCCESS_SIGNALS)
    form_gone = not await page.query_selector('form')

    confirmed = url_changed or success_text or form_gone
    print(f"  [verify] url_changed={url_changed} success_text={success_text} form_gone={form_gone} → {'CONFIRMED' if confirmed else 'UNCONFIRMED'}")
    return confirmed
