import pytest
from selenium import webdriver
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.company_item import CompanyItem
from src.scrapers import Scrapers


@pytest.fixture
def driver():
    """Fixture to create and tear down a Chrome WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture
def scraper():
    """Fixture to create a ScrapeAshbyhq instance."""
    return ScrapeAshbyhq()


@pytest.fixture
def company():
    """Fixture to create a Nethermind CompanyItem."""
    return CompanyItem("nethermind", "https://jobs.ashbyhq.com/nethermind", Scrapers.ASHBYHQ, "https://nethermind.io")


def test_ashbyhq_scraper_nethermind(driver, scraper, company):
    """Test AshbyHQ scraper with Nethermind to verify job extraction."""
    # Act
    jobs = scraper.getJobs(driver, company.jobs_url, company.company_name)
    
    # Assert
    assert isinstance(jobs, list), "getJobs should return a list"
    assert len(jobs) > 0, f"Expected jobs for {company.company_name}, but got none"
    
    # Verify structure of each job
    for job in jobs:
        assert "company" in job, "Job missing 'company' field"
        assert "title" in job, "Job missing 'title' field"
        assert "link" in job, "Job missing 'link' field"
        assert "location" in job, "Job missing 'location' field"
        
        assert job["company"] == company.company_name, f"Company name mismatch"
        assert isinstance(job["title"], str) and len(job["title"]) > 0, "Job title should be non-empty string"
        assert job["link"].startswith("http"), "Job link should be a valid URL"
        assert isinstance(job["location"], str) and len(job["location"]) > 0, "Location should be non-empty string"
        
        # Verify location cleaning worked (should not contain newlines)
        assert "\n" not in job["location"], "Location should not contain newlines"
        
        # Verify link contains ashbyhq
        assert "ashbyhq.com" in job["link"], "Job link should be from AshbyHQ"
