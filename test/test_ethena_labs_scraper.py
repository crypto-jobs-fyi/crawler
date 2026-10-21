# Run: pytest -q -s --run-live test/test_ethena_labs_scraper.py

import json

from src.scrape_ethena_labs import ScrapeEthenaLabs


def test_ethena_labs_scraper(page_adapter):
    company = "ethenalabs"
    jobs_url = "https://careers.ethena.fi/jobs"

    jobs = ScrapeEthenaLabs().getJobs(page_adapter, jobs_url, company)
    print(json.dumps({"job_count": len(jobs), "jobs": jobs}, indent=2))

    assert jobs
    assert all(set(job) == {"company", "title", "location", "link"} for job in jobs)
    known_job = next(
        (
            job
            for job in jobs
            if job["title"] == "Customer Success Manager - Ethena Pay"
        ),
        None,
    )
    assert known_job is not None
    assert known_job["company"] == company
    assert known_job["location"] == "Fully Remote"
    assert (
        known_job["link"]
        == "https://careers.ethena.fi/jobs/8495362-customer-success-manager-ethena-pay"
    )
