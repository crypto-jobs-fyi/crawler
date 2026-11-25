import pytest

from src.company_item import CompanyItem
from src.scrape_oxylabs import ScrapeOxylabs
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeOxylabs()


@pytest.fixture
def company():
    return CompanyItem(
        "oxylabs",
        "https://career.oxylabs.io/#jobs",
        Scrapers.OXYLABS,
        "https://www.oxylabs.io",
    )


def test_oxylabs_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["location"]
        assert job["link"].startswith("http")
