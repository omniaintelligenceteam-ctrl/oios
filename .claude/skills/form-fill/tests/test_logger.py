# tests/test_logger.py
import pytest, os, csv, tempfile
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from logger import log_attempt, FIELDNAMES

def test_log_attempt_creates_file_with_header(tmp_path):
    log_file = str(tmp_path / "log.csv")
    log_attempt(log_file, company_name="Acme", site_url="https://acme.com",
                contact_method="form", job_title="Receptionist", status="submitted")
    with open(log_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]['company_name'] == 'Acme'
    assert rows[0]['status'] == 'submitted'

def test_log_attempt_appends_rows(tmp_path):
    log_file = str(tmp_path / "log.csv")
    log_attempt(log_file, company_name="A", site_url="x", contact_method="form", job_title="r", status="submitted")
    log_attempt(log_file, company_name="B", site_url="y", contact_method="email", job_title="r", status="email-only")
    with open(log_file) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[1]['company_name'] == 'B'
