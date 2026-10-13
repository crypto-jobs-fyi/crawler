from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from src.playwright_scrape_it import PlaywrightScrapeIt


class ScrapeAvaraPlaywright(PlaywrightScrapeIt):
    name = "Avara"

    def getJobs(self, page: Page, web_page: str, company: str = "avara") -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)

        accept_all = page.get_by_role("button", name="Accept All", exact=True)
        if accept_all.count():
            try:
                accept_all.first.click(timeout=5_000)
            except PlaywrightError as error:
                self.log_warning("Cookie consent failed", company=company, error=str(error))

        jobs = page.locator('li a[href*="/careers/"]')
        result = []
        for index in range(jobs.count()):
            job = jobs.nth(index)
            result.append(
                {
                    "company": company,
                    "title": self._text(job.locator("div")),
                    "location": "Remote or Hybrid",
                    "link": self._href(job, page.url),
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
