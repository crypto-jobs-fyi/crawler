import pytest

from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_avara import ScrapeAvara
from src.scrape_coinbase import ScrapeCoinbase
from src.scrape_kula import ScrapeKula
from src.scrape_revolut_people import ScrapeRevolutPeople
from src.scrape_robinhood import ScrapeRobinhood
from src.scrape_sygnum import ScrapeSygnum


def serve_html(page, html: str) -> None:
    page.route(
        "**/*",
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body=html,
        ),
    )
    page.goto("https://playwright.test/jobs")


def assert_job(job: dict, company: str) -> None:
    assert job["company"] == company
    assert job["title"]
    assert job["location"]
    assert job["link"].startswith("https://playwright.test/")


@pytest.mark.parametrize(
    ("scraper", "company", "html"),
    [
        (
            ScrapeCoinbase,
            "coinbase",
            """
            <div data-testid="positions-department">
                <button>Engineering</button>
            </div>
            <a href="/careers/positions/123">
                <span>Senior Engineer</span><span>Remote</span>
            </a>
            """,
        ),
        (
            ScrapeSygnum,
            "sygnum",
            """
            <button>Accept</button>
            <ul>
                <li class="results-list__item result-item">
                    <h3><a href="/jobs/123">Backend Engineer</a></h3>
                    <p class="result-item__location">United States</p>
                </li>
            </ul>
            """,
        ),
        (
            ScrapeKula,
            "paradigm.co",
            """
            <div class="chakra-card">
                <div class="chakra-stack">
                    <p class="chakra-text">Protocol Engineer</p>
                    <p class="chakra-text">New York, New York</p>
                </div>
                <a class="chakra-link" href="/jobs/123">View job</a>
            </div>
            """,
        ),
        (
            ScrapeAvara,
            "avara",
            """
            <button>Accept All</button>
            <ul>
                <li><a href="/careers/123"><div>Product Engineer</div></a></li>
            </ul>
            """,
        ),
        (
            ScrapeRobinhood,
            "robinhood",
            """
            <div data-filter="engineering" class="accordion">Engineering</div>
            <div id="jobs-data"></div>
            <script>
                setTimeout(() => {
                    document.querySelector("#jobs-data").innerHTML =
                        '<p class="job" data-location="Remote"><a href="/jobs/123">Staff Engineer</a></p>';
                }, 50);
            </script>
            """,
        ),
        (
            ScrapeRevolutPeople,
            "huspy",
            """
            <button><span>Allow all cookies</span></button>
            <a aria-label="position-link" href="/jobs/123">
                <span><span>Senior Product Manager</span></span>
                <div data-testid="location-row">Dubai, UAE</div>
                <div data-testid="location-row">United Arab Emirates</div>
            </a>
            """,
        ),
    ],
)
def test_headed_scraper_contract(page, scraper, company, html):
    serve_html(page, html)

    jobs = scraper().getJobs(
        PlaywrightPageAdapter(page),
        "https://playwright.test/jobs",
        company,
    )

    assert len(jobs) == 1
    assert_job(jobs[0], company)


def test_coinbase_extracts_location_from_combined_card_text(page):
    serve_html(
        page,
        """
        <div data-testid="positions-department">
            <button>Operations</button>
        </div>
        <div class="job-card">
            <a href="/careers/positions/7980600">
                Business Operations Senior Associate, Institutional
            </a>
            <span>Business Operations Senior Associate, InstitutionalRemote - USA</span>
        </div>
        """,
    )

    jobs = ScrapeCoinbase().getJobs(
        PlaywrightPageAdapter(page),
        "https://playwright.test/jobs",
        "coinbase",
    )

    assert jobs[0]["title"] == "Business Operations Senior Associate, Institutional"
    assert jobs[0]["location"] == "Remote - USA"
