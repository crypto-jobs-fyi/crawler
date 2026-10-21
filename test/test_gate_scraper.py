# Run: pytest -q -s --run-live test/test_gate_scraper.py

import json

from src.scrape_gate import ScrapeGate


def test_gate_scraper(page_adapter):
    company = "gate.io"
    jobs_url = "https://www.gate.com/careers/jobs"

    jobs = ScrapeGate().getJobs(page_adapter, jobs_url, company)
    print(json.dumps({"job_count": len(jobs), "jobs": jobs}, indent=2))

    assert jobs
    assert all(set(job) == {"company", "title", "location", "link"} for job in jobs)
    known_job = next(
        (
            job
            for job in jobs
            if job["title"] == "Core Trading System Developer"
        ),
        None,
    )
    assert known_job is not None
    assert known_job["company"] == company
    assert known_job["location"] == "Remote"
    assert (
        known_job["link"]
        == "https://www.gate.com/careers/jobs/core-trading-system-developer-764"
    )
