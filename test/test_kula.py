import pytest
from src.scrape_kula import ScrapeKula
from src.company_item import CompanyItem
from src.scrapers import Scrapers




@pytest.fixture
def scraper():
    """Fixture to create a ScrapeKula instance."""
    return ScrapeKula()


@pytest.fixture
def company():
    """Fixture to create a Paradigm CompanyItem."""
    return CompanyItem('paradigm.co', 'https://careers.kula.ai/paradigm', Scrapers.KULA, 'https://www.paradigm.co')


def test_kula_scraper(page_adapter, scraper, company):
    """Test Kula scraper with Paradigm to verify job extraction."""
    # Act
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)
    
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
