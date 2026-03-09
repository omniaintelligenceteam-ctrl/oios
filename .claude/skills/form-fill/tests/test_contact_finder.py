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
