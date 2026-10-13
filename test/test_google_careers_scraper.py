# Run: pytest -q -s --run-live test/test_google_careers_scraper.py
import json

import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.playwright_adapter import PlaywrightWait
from src.scrape_google_careers import ScrapeGoogleCareers


class FakePage:
    def __init__(self, script_result):
        self.script_result = script_result
        self.wait_seconds = None
        self.loaded_url = None
        self.execute_script_calls = 0
        self.last_script = None

    def implicitly_wait(self, seconds):
        self.wait_seconds = seconds

    def get(self, url):
        self.loaded_url = url

    def execute_script(self, script, selector):
        self.execute_script_calls += 1
        self.last_script = script
        assert selector == ScrapeGoogleCareers.JOB_LINK_SELECTOR
        return self.script_result


def test_google_careers_scraper_deduplicates_and_filters(monkeypatch):
    monkeypatch.setattr(PlaywrightWait, "until", lambda self, condition: True)
    scraper = ScrapeGoogleCareers()
    page_adapter = FakePage([
        {"href": "https://careers.google.com/jobs/1", "title": "Research Engineer", "location": "London, UK"},
        {"href": "https://careers.google.com/jobs/1", "title": "Research Engineer", "location": "London, UK"},
        {"href": "https://careers.google.com/jobs/2", "title": "", "location": "Paris, France"},
        {"href": "https://careers.google.com/jobs/3", "title": "Research Scientist", "location": ""},
    ])

    jobs = scraper.getJobs(page_adapter, "https://example.com/jobs", "deepmind")

    assert page_adapter.wait_seconds == 10
    assert page_adapter.loaded_url == "https://example.com/jobs"
    assert len(jobs) == 2
    assert jobs[0]["title"] == "Research Engineer"
    assert jobs[0]["location"] == "London, UK"
    assert jobs[1]["title"] == "Research Scientist"
    assert jobs[1]["location"] == "Unknown"
    assert page_adapter.execute_script_calls == 1
    assert "querySelectorAll(linkSelector)" in page_adapter.last_script
    assert "h2, h3, h4" in page_adapter.last_script
    assert '[aria-label*="location"]' in page_adapter.last_script


def test_google_careers_scraper_returns_empty_on_timeout(monkeypatch):
    def _raise_timeout(self, condition):
        raise TimeoutError("timed out")

    monkeypatch.setattr(PlaywrightWait, "until", _raise_timeout)
    scraper = ScrapeGoogleCareers()
    page_adapter = FakePage([
        {"href": "https://careers.google.com/jobs/1", "title": "Should Not Be Used", "location": "Remote"},
    ])

    jobs = scraper.getJobs(page_adapter, "https://example.com/jobs", "deepmind")

    assert jobs == []
    assert page_adapter.execute_script_calls == 0


def test_google_careers_scraper_keeps_valid_duplicate_after_empty_title(monkeypatch):
    monkeypatch.setattr(PlaywrightWait, "until", lambda self, condition: True)
    scraper = ScrapeGoogleCareers()
    page_adapter = FakePage([
        {"href": "https://careers.google.com/jobs/9", "title": "", "location": "Remote"},
        {"href": "https://careers.google.com/jobs/9", "title": "Research Lead", "location": "Remote"},
    ])

    jobs = scraper.getJobs(page_adapter, "https://example.com/jobs", "deepmind")

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Research Lead"
    assert jobs[0]["link"] == "https://careers.google.com/jobs/9"


def test_google_careers_scraper_prefers_specific_title_for_duplicate(monkeypatch):
    monkeypatch.setattr(PlaywrightWait, "until", lambda self, condition: True)
    scraper = ScrapeGoogleCareers()
    page_adapter = FakePage([
        {"href": "https://careers.google.com/jobs/7", "title": "Apply", "location": "Unknown"},
        {"href": "https://careers.google.com/jobs/7", "title": "Senior Research Engineer", "location": "Unknown"},
    ])

    jobs = scraper.getJobs(page_adapter, "https://example.com/jobs", "deepmind")

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Senior Research Engineer"


def test_google_careers_scraper_live(page, request):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live Google Careers test; pass --run-live to execute it.")

    jobs = ScrapeGoogleCareers().getJobs(
        PlaywrightPageAdapter(page),
        "https://www.google.com/about/careers/applications/jobs/results"
        "?company=DeepMind",
        "deepmind",
    )

    print(json.dumps({"job_cards": len(jobs), "jobs": jobs}, indent=2))
    assert jobs
    assert all(job["company"] == "deepmind" for job in jobs)
