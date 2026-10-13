import pytest

from src.playwright_adapter import PlaywrightPageAdapter


def pytest_addoption(parser):
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run scraper tests against live job sites.",
    )


@pytest.fixture
def driver(request, page):
    if not request.config.getoption("--run-live"):
        pytest.skip("Live scraper test; pass --run-live to execute it.")
    return PlaywrightPageAdapter(page)
