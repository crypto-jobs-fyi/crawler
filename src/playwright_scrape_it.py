from abc import abstractmethod
from urllib.parse import urljoin

from playwright.sync_api import Page

from src.scrape_it import ScrapeIt


class PlaywrightScrapeIt(ScrapeIt):
    @abstractmethod
    def getJobs(self, page: Page, web_page: str, company: str) -> list[dict]:
        pass

    @staticmethod
    def _text(locator, default: str = "") -> str:
        return locator.inner_text().strip() if locator.count() else default

    @staticmethod
    def _href(locator, base_url: str = "", default: str = "") -> str:
        href = locator.get_attribute("href") or default
        return urljoin(base_url, href) if base_url else href
