import json
import pytest
from selenium import webdriver
from src.scrape_cursor import ScrapeCursor
from src.company_item import CompanyItem
from src.scrapers import Scrapers


@pytest.fixture
def driver():
    """Fixture to create and tear down a Chrome WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture
def scraper():
    """Fixture to create a ScrapeCursor instance."""
    return ScrapeCursor()


@pytest.fixture
def company():
    """Fixture to create a Cursor CompanyItem."""
    return CompanyItem("cursor", "https://cursor.com/careers", Scrapers.CURSOR,
                       "https://cursor.com")


# pytest test/test_cursor_scraper.py::test_cursor_scraper
def test_cursor_scraper(driver, scraper, company):
    """Test Cursor scraper to verify job extraction."""
    # Act
    jobs = scraper.getJobs(driver, company.jobs_url, company.company_name)
    with open("cursor_jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    # Assert
    assert isinstance(jobs, list), "getJobs should return a list"
    assert len(jobs) >= 1, f"Expected at least 1 job for {company.company_name}, but got {len(jobs)}"

    # Verify structure of each job
    for job in jobs:
        assert "company" in job, "Job missing 'company' field"
        assert "title" in job, "Job missing 'title' field"
        assert "link" in job, "Job missing 'link' field"
        assert "location" in job, "Job missing 'location' field"

        assert job["company"] == company.company_name, "Company name mismatch"
        assert isinstance(job["title"], str) and len(job["title"]) > 0, "Job title should be non-empty string"
        assert job["link"].startswith("http"), "Job link should be a valid URL"
        assert isinstance(job["location"], str), "Location should be a string"
