import pytest

from src.company_item import CompanyItem
from src.scrape_rentec import ScrapeRentec
from src.scrapers import Scrapers


@pytest.fixture
def scraper():
    return ScrapeRentec()


@pytest.fixture
def company():
    return CompanyItem(
        "rentec",
        "https://www.rentec.com/Careers.action?jobs=true",
        Scrapers.RENTEC,
        "https://www.rentec.com",
    )


def test_rentec_scraper(page_adapter, scraper, company):
    jobs = scraper.getJobs(page_adapter, company.jobs_url, company.company_name)

    assert jobs
    for job in jobs:
        assert job["company"] == company.company_name
        assert job["title"]
        assert job["location"]
        assert job["link"].startswith("http")
