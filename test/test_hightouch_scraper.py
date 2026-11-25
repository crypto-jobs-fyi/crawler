import pytest

from src.company_item import CompanyItem
from src.scrape_hightouch import ScrapeHightouch
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeHightouch()


@pytest.fixture
def company():
    return CompanyItem(
        "hightouch",
        "https://hightouch.com/careers#open-positions",
        Scrapers.HIGHTOUCH,
        "https://hightouch.com",
    )


def test_hightouch_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["location"]
        assert job["link"].startswith("http")
