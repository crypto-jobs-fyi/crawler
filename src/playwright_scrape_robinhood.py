from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.playwright_scrape_it import PlaywrightScrapeIt


class ScrapeRobinhoodPlaywright(PlaywrightScrapeIt):
    name = "robinhood"

    def getJobs(self, page: Page, web_page: str, company: str = "robinhood") -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)

        jobs = page.locator("#jobs-data p.job")
        try:
            jobs.first.wait_for(state="attached", timeout=30_000)
        except PlaywrightTimeoutError:
            self.log_warning(
                "Job listings did not load",
                company=company,
                web_page=web_page,
                selector="#jobs-data p.job",
            )

        accept_all = page.locator("#ip-user-consent-accept")
        if accept_all.count():
            try:
                accept_all.first.click(timeout=5_000)
            except PlaywrightError as error:
                self.log_warning("Cookie consent failed", company=company, error=str(error))

        departments = page.locator('div[data-filter][class*="accordion"]')
        for index in range(departments.count()):
            try:
                departments.nth(index).click(timeout=5_000)
            except PlaywrightError as error:
                self.log_warning(
                    "Department expansion failed",
                    company=company,
                    department_index=index,
                    error=str(error),
                )

        result = []
        for index in range(jobs.count()):
            job = jobs.nth(index)
            title_link = job.locator("a")
            result.append(
                {
                    "company": company,
                    "title": self._text(title_link),
                    "location": job.get_attribute("data-location") or "",
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
