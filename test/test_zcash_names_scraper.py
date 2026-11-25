import pytest

from src.company_item import CompanyItem
from src.scrape_zcash_names import ScrapeZcashNames
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeZcashNames()


@pytest.fixture
def company():
    return CompanyItem(
        "zcashnames",
        "https://www.zcashnames.com/careers",
        Scrapers.ZCASH_NAMES,
        "https://www.zcashnames.com",
    )


def test_zcash_names_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["link"].startswith("http")
