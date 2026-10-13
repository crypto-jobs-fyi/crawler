from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.playwright_scrape_it import PlaywrightScrapeIt


class ScrapeRevolutPeoplePlaywright(PlaywrightScrapeIt):
    name = "Cleo"

    @staticmethod
    def clean_location(location: str) -> str:
        return (
            location.strip()
            .replace("United States", "US")
            .replace("United Kingdom", "UK")
            .replace("United Arab Emirates", "UAE")
            .replace("\n", " ")
        )

    def getJobs(
        self,
        page: Page,
        web_page: str,
        company: str = "Cleo",
    ) -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)

        jobs = page.locator('a[aria-label="position-link"]')
        try:
            jobs.first.wait_for(state="attached", timeout=30_000)
        except PlaywrightTimeoutError:
            self.log_warning(
                "Job listings did not load",
                company=company,
                web_page=web_page,
                selector='a[aria-label="position-link"]',
            )

        cookie_banner = page.get_by_role(
            "button",
            name="Allow all cookies",
            exact=True,
        )
        if cookie_banner.count():
            try:
                cookie_banner.first.click(timeout=5_000)
            except PlaywrightError as error:
                self.log_warning(
                    "Accept cookies failed",
                    company=company,
                    error=str(error),
                )

        result = []
        for index in range(jobs.count()):
            job = jobs.nth(index)
            title_lines = self._text(job.locator("span span").first).splitlines()
            title = title_lines[0].strip() if title_lines else ""
            locations = job.locator('div[data-testid="location-row"]')
            location = (
                self.clean_location(self._text(locations.nth(locations.count() - 1)))
                if locations.count()
                else "UK"
            )
            result.append(
                {
                    "company": company,
                    "title": title,
                    "location": location,
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
