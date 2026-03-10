# learner.py
"""
Analyzes form-fill log after each run and updates learnings.json.
Learnings are loaded at the start of the next run to improve success rate.
"""
import json
import csv
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

LEARNINGS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', 'form-fill', 'learnings.json')

def load_learnings() -> dict:
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE) as f:
            return json.load(f)
    return {
        "blocked_domains": [],
        "no_form_domains": [],
        "successful_domains": [],
        "contacted_domains": [],
        "failure_reasons": {},
        "total_runs": 0,
        "total_submitted": 0,
        "total_failed": 0,
        "last_updated": None
    }

def save_learnings(learnings: dict):
    os.makedirs(os.path.dirname(LEARNINGS_FILE), exist_ok=True)
    learnings["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(LEARNINGS_FILE, 'w') as f:
        json.dump(learnings, f, indent=2)

def update_learnings(log_file: str):
    """Read the log and update learnings.json."""
    if not os.path.exists(log_file):
        return

    learnings = load_learnings()
    learnings["total_runs"] += 1

    with open(log_file, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        domain = urlparse(row.get('site_url', '')).netloc
        status = row.get('status', '')

        if status == 'submitted':
            learnings['total_submitted'] += 1
            if domain:
                if domain not in learnings['successful_domains']:
                    learnings['successful_domains'].append(domain)
                if domain not in learnings.setdefault('contacted_domains', []):
                    learnings['contacted_domains'].append(domain)
        elif status == 'submitted-unconfirmed':
            learnings['total_submitted'] += 1
            if domain and domain not in learnings.setdefault('contacted_domains', []):
                learnings['contacted_domains'].append(domain)
        elif 'failed' in status:
            learnings['total_failed'] += 1
            reason = status.replace('failed: ', '')
            learnings['failure_reasons'][reason] = learnings['failure_reasons'].get(reason, 0) + 1
            if 'blocked' in reason.lower() or 'timeout' in reason.lower():
                if domain and domain not in learnings['blocked_domains']:
                    learnings['blocked_domains'].append(domain)
        elif status == 'no-contact-found':
            if domain and domain not in learnings['no_form_domains']:
                learnings['no_form_domains'].append(domain)

    save_learnings(learnings)
    _print_summary(learnings)

def _print_summary(learnings: dict):
    total = learnings['total_submitted'] + learnings['total_failed']
    rate = round(learnings['total_submitted'] / total * 100) if total > 0 else 0
    print(f"\n[learner] Lifetime stats: {learnings['total_submitted']} submitted / {total} attempted ({rate}% success rate)")
    if learnings['failure_reasons']:
        top = sorted(learnings['failure_reasons'].items(), key=lambda x: -x[1])[:3]
        # Strip non-ASCII to avoid charmap errors on Windows terminals
        reasons_str = ', '.join(f"{r.encode('ascii', 'replace').decode()} ({n}x)" for r, n in top)
        print(f"[learner] Top failure reasons: {reasons_str}")
    print(f"[learner] Learnings saved to learnings.json\n")
