# logger.py
import csv
import os
from datetime import datetime

FIELDNAMES = ['timestamp', 'company_name', 'site_url', 'contact_method', 'job_title', 'status']

def log_attempt(log_file: str, company_name: str, site_url: str,
                contact_method: str, job_title: str, status: str):
    if os.path.dirname(log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    write_header = not os.path.exists(log_file)
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.utcnow().isoformat(),
            'company_name': company_name,
            'site_url': site_url,
            'contact_method': contact_method,
            'job_title': job_title,
            'status': status,
        })
