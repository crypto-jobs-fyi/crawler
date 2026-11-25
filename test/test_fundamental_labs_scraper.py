import pytest

from src.company_item import CompanyItem
from src.scrape_fundamental_labs import ScrapeFundamentalLabs
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeFundamentalLabs()


@pytest.fixture
def company():
    return CompanyItem(
        "FundamentalLabs",
        "https://fundamentalresearchlabs.com/careers",
        Scrapers.FUNDAMENTAL_LABS,
        "https://fundamentalresearchlabs.com",
    )


def test_fundamental_labs_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["location"]
        assert job["link"].startswith("http")
