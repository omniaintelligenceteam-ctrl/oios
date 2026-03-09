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
