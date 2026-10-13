from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from src.playwright_scrape_it import PlaywrightScrapeIt


class ScrapeSygnumPlaywright(PlaywrightScrapeIt):
    name = "Sygnum"

    def _click_if_present(self, page: Page, selector: str, company: str) -> None:
        locator = page.locator(selector)
        if not locator.count():
            return
        try:
            locator.first.click(timeout=5_000)
        except PlaywrightError as error:
            self.log_warning(
                "Optional page interaction failed",
                company=company,
                selector=selector,
                error=str(error),
            )

    def getJobs(self, page: Page, web_page: str, company: str = "sygnum") -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)
        self._click_if_present(page, 'button:has-text("Accept")', company)
        self._click_if_present(page, 'a:has-text("CONTINUE")', company)
        self._click_if_present(page, 'a:has-text("Close")', company)

        jobs = page.locator("ul li.results-list__item.result-item")
        result = []
        for index in range(jobs.count()):
            job = jobs.nth(index)
            title_link = job.locator("h3 a")
            location = self._text(job.locator("p.result-item__location"))
            result.append(
                {
                    "company": company,
                    "title": self._text(title_link),
                    "location": location.replace("United States", "US")
                    .replace("United Kingdom", "UK")
                    .replace("United Arab Emirates", "UAE"),
                    "link": self._href(title_link, page.url),
                }
            )

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=jobs.count(),
            jobs_scraped=len(result),
        )
        return result
