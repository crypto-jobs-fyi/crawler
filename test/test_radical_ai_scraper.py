# Run: pytest -q -s --run-live test/test_radical_ai_scraper.py

import json

from src.scrape_radical_ai import ScrapeRadicalAI


def test_radical_ai_scraper(page_adapter):
    company = "RadicalAI"
    jobs_url = "https://app.nodi.global/company/radical%20ai"

    jobs = ScrapeRadicalAI().getJobs(page_adapter, jobs_url, company)
    print(json.dumps({"job_count": len(jobs), "jobs": jobs}, indent=2))

    assert jobs
    assert all(set(job) == {"company", "title", "location", "link"} for job in jobs)
    assert all(job["company"] == company for job in jobs)
    assert all(job["title"].strip() for job in jobs)
    assert all(job["location"].strip() for job in jobs)
    assert all(
        job["link"].startswith("https://app.nodi.global/jobs/public/")
        for job in jobs
    )
