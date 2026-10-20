# Run: pytest -q -s --run-live test/test_binance_scraper.py
import json

import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_binance import ScrapeBinance


def test_binance_scraper_live(page, request):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live Binance test; pass --run-live to execute it.")

    jobs = ScrapeBinance().getJobs(
        PlaywrightPageAdapter(page),
        "https://www.binance.com/en/careers/job-openings",
        "binance",
    )

    print(json.dumps({"job_cards": len(jobs), "jobs": jobs}, indent=2))
    assert jobs
    assert all(set(job) == {"company", "title", "location", "link"} for job in jobs)
    assert all(job["company"] == "binance" for job in jobs)
    assert all(job["link"].startswith("https://www.binance.com/en/careers/job?id=") for job in jobs)

    known_job = next(
        (job for job in jobs if job["title"] == "Affiliate BD - APAC"),
        None,
    )
    assert known_job is not None
    assert known_job["location"] == "Hong Kong; Korea, Republic of; Taiwan"
    assert known_job["link"] == "https://www.binance.com/en/careers/job?id=5004800101"
