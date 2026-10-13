import pytest
from src.scrape_gemini import ScrapeGemini
from src.company_item import CompanyItem
from src.scrapers import Scrapers




@pytest.fixture
def scraper():
    """Fixture to create a ScrapeGemini instance."""
    return ScrapeGemini()


@pytest.fixture
def company():
    """Fixture to create a Gemini CompanyItem."""
    return CompanyItem("gemini", "https://www.gemini.com/careers", Scrapers.GEMINI, "https://www.gemini.com")


def test_gemini_scraper(page_adapter, scraper, company):
    """Test Gemini scraper to verify job extraction."""
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
        
        # Verify location cleaning worked (should not contain newlines)
        assert "\n" not in job["location"], "Location should not contain newlines"
