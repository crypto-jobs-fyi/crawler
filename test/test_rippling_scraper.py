# Run: pytest -q -s --run-live test/test_rippling_scraper.py

import json

import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_rippling import ScrapeRippling


def test_rippling_scraper(page, request):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live scraper test; pass --run-live to execute it.")

    jobs = ScrapeRippling().getJobs(
        PlaywrightPageAdapter(page),
        "https://ats.rippling.com/en-US/plume-network/jobs",
        "plume",
    )
    print(json.dumps({"job_cards": len(jobs), "jobs": jobs}, indent=2))

    assert len(jobs) >= 10
    known_job = next(
        job
        for job in jobs
        if job["link"].endswith(
            "/plume-network/jobs/2d063450-5a60-407f-82e1-c44ed688998e"
        )
    )
    assert known_job["title"] == "Business Development Director"
    assert known_job["location"] == "Remote (United States)"
    assert known_job["link"].startswith("https://ats.rippling.com/")
