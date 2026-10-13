# Run: pytest -q -s --run-live test/test_dayforce_scraper.py
import json

import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_dayforce import ScrapeDayforce


def test_dayforce_scraper_extracts_title_location_and_link(page, request):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live Dayforce test; pass --run-live to execute it.")

    jobs = ScrapeDayforce().getJobs(
        PlaywrightPageAdapter(page),
        "https://jobs.dayforcehcm.com/en-US/ibgllc/CANDIDATEPORTAL",
        "interactivebrokers",
    )
    print(json.dumps({"job_cards": len(jobs), "jobs": jobs}, indent=2))

    job = next(
        job for job in jobs
        if job["link"].rstrip("/").endswith("/jobs/2642")
    )
    assert job["title"] == "Technical Assistance Associate"
    assert job["location"] == "Shanghai, China"
