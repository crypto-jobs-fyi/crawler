import json

import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_revolut import ScrapeRevolut


def test_revolut_scraper(browser_type, request):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live scraper test; pass --run-live to execute it.")

    browser = browser_type.launch(headless=False)
    page = browser.new_page()
    try:
        jobs = ScrapeRevolut().getJobs(
            PlaywrightPageAdapter(page),
            "https://www.revolut.com/careers/",
            "revolut",
        )
    finally:
        browser.close()

    print(json.dumps({"job_cards": len(jobs), "jobs": jobs}, indent=2))

    assert len(jobs) >= 300
    known_job = next(
        job
        for job in jobs
        if job["link"].endswith(
            "/careers/position/credit-manager-policy-531a667a-805b-47c8-8749-cc0e536ed122/"
        )
    )
    assert known_job["title"] == "Credit Manager (Policy)"
    assert known_job["location"] == "Remote: Brazil; Office: Sao Paulo"
