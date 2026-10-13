import pytest

from src.playwright_scrape_avara import ScrapeAvaraPlaywright
from src.playwright_scrape_coinbase import ScrapeCoinbasePlaywright
from src.playwright_scrape_kula import ScrapeKulaPlaywright
from src.playwright_scrape_robinhood import ScrapeRobinhoodPlaywright
from src.playwright_scrape_sygnum import ScrapeSygnumPlaywright


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
            ScrapeCoinbasePlaywright,
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
            ScrapeSygnumPlaywright,
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
            ScrapeKulaPlaywright,
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
            ScrapeAvaraPlaywright,
            "avara",
            """
            <button>Accept All</button>
            <ul>
                <li><a href="/careers/123"><div>Product Engineer</div></a></li>
            </ul>
            """,
        ),
        (
            ScrapeRobinhoodPlaywright,
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
    ],
)
def test_headed_scraper_contract(page, scraper, company, html):
    serve_html(page, html)

    jobs = scraper().getJobs(page, "https://playwright.test/jobs", company)

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

    jobs = ScrapeCoinbasePlaywright().getJobs(
        page,
        "https://playwright.test/jobs",
        "coinbase",
    )

    assert jobs[0]["title"] == "Business Operations Senior Associate, Institutional"
    assert jobs[0]["location"] == "Remote - USA"
