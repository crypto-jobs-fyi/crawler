from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from src.scrape_google_careers import ScrapeGoogleCareers


class FakeDriver:
    def __init__(self, script_result):
        self.script_result = script_result
        self.wait_seconds = None
        self.loaded_url = None
        self.execute_script_calls = 0

    def implicitly_wait(self, seconds):
        self.wait_seconds = seconds

    def get(self, url):
        self.loaded_url = url

    def execute_script(self, script, selector):
        self.execute_script_calls += 1
        assert selector == ScrapeGoogleCareers.JOB_LINK_SELECTOR
        return self.script_result


def test_google_careers_scraper_deduplicates_and_filters(monkeypatch):
    monkeypatch.setattr(WebDriverWait, "until", lambda self, condition: True)
    scraper = ScrapeGoogleCareers()
    driver = FakeDriver([
        {"href": "https://careers.google.com/jobs/1", "title": "Research Engineer", "location": "London, UK"},
        {"href": "https://careers.google.com/jobs/1", "title": "Research Engineer", "location": "London, UK"},
        {"href": "https://careers.google.com/jobs/2", "title": "", "location": "Paris, France"},
        {"href": "https://careers.google.com/jobs/3", "title": "Research Scientist", "location": ""},
    ])

    jobs = scraper.getJobs(driver, "https://example.com/jobs", "deepmind")

    assert driver.wait_seconds == 10
    assert driver.loaded_url == "https://example.com/jobs"
    assert len(jobs) == 2
    assert jobs[0]["title"] == "Research Engineer"
    assert jobs[0]["location"] == "London, UK"
    assert jobs[1]["title"] == "Research Scientist"
    assert jobs[1]["location"] == "Unknown"


def test_google_careers_scraper_returns_empty_on_timeout(monkeypatch):
    def _raise_timeout(self, condition):
        raise TimeoutException("timed out")

    monkeypatch.setattr(WebDriverWait, "until", _raise_timeout)
    scraper = ScrapeGoogleCareers()
    driver = FakeDriver([
        {"href": "https://careers.google.com/jobs/1", "title": "Should Not Be Used", "location": "Remote"},
    ])

    jobs = scraper.getJobs(driver, "https://example.com/jobs", "deepmind")

    assert jobs == []
    assert driver.execute_script_calls == 0
