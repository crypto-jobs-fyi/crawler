import pytest

from src.company_item import CompanyItem
from src.scrape_workato import ScrapeWorkato
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeWorkato()


@pytest.fixture
def company():
    return CompanyItem(
        "workato",
        "https://www.workato.com/careers#open-roles",
        Scrapers.WORKATO,
        "https://www.workato.com",
    )


def test_workato_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["location"]
        assert job["link"].startswith("http")
