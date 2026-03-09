# tests/test_job_scraper.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from job_scraper import parse_indeed_results, JobListing
import asyncio

def test_parse_indeed_results_extracts_fields():
    html = """
    <div class="job_seen_beacon">
        <span class="companyName">Acme Corp</span>
        <h2 class="jobTitle"><span>Office Manager</span></h2>
        <span class="companyLocation">Austin, TX</span>
    </div>
    """
    results = parse_indeed_results(html)
    assert len(results) == 1
    assert results[0].company_name == "Acme Corp"
    assert results[0].job_title == "Office Manager"

def test_parse_indeed_results_empty_html():
    results = parse_indeed_results("<html></html>")
    assert results == []

def test_job_listing_dataclass():
    job = JobListing(company_name="Test Co", job_title="Receptionist", company_website="", source="indeed")
    assert job.company_name == "Test Co"
    assert job.status == "pending"
