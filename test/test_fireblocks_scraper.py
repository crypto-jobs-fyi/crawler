# Run: pytest -q -s --run-live test/test_fireblocks_scraper.py

import json

from src.scrape_fireblocks import ScrapeFireblocks


def test_fireblocks_scraper(page_adapter):
    company = "fireblocks"
    jobs_url = "https://www.fireblocks.com/careers#open-roles"

    jobs = ScrapeFireblocks().getJobs(page_adapter, jobs_url, company)
    print(json.dumps({"job_count": len(jobs), "jobs": jobs}, indent=2))

    assert jobs
    assert all(set(job) == {"company", "title", "location", "link"} for job in jobs)
    assert all(job["company"] == company for job in jobs)
    assert all(job["title"].strip() for job in jobs)
    assert all(job["location"].strip() for job in jobs)
    assert all(
        job["link"].startswith("https://www.fireblocks.com/careers/positions/")
        for job in jobs
    )
