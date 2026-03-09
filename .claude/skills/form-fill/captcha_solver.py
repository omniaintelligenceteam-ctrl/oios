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
