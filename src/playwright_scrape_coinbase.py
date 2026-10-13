from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from src.playwright_scrape_it import PlaywrightScrapeIt


class ScrapeCoinbasePlaywright(PlaywrightScrapeIt):
    name = "Coinbase"

    def getJobs(self, page: Page, web_page: str, company: str = "coinbase") -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)

        page.evaluate(
            """
            () => {
                document.querySelectorAll('[id*="cookie"], [class*="cookie"], [id*="consent"], [class*="consent"], [role="dialog"], .modal, .overlay, [aria-modal="true"], [class*="backdrop"], [id*="backdrop"]').forEach((element) => element.remove());
                document.body.style.overflow = "auto";
                document.documentElement.style.overflow = "auto";
                document.body.style.height = "auto";
            }
            """
        )

        departments = page.locator('[data-testid="positions-department"] button')
        if not departments.count():
            departments = page.locator('[data-testid="positions-department"]')

        for index in range(departments.count()):
            try:
                department = departments.nth(index)
                department.scroll_into_view_if_needed()
                department.click(force=True, timeout=5_000)
            except PlaywrightError as error:
                self.log_warning(
                    "Department expansion failed",
                    company=company,
                    department_index=index,
                    error=str(error),
                )

        page.wait_for_timeout(1_000)
        job_links = page.locator('a[href*="/careers/positions/"]')
        result = []
        excluded_patterns = (
            "/login",
            "/signup",
            "/about",
            "/blog",
            "/press",
            "/security",
            "/investors",
            "/vendors",
            "/legal",
            "/cookie",
            "/affiliates",
            "/terms",
            "/privacy",
            "e-verify",
            "eeoc",
            "chromevox",
        )

        for index in range(job_links.count()):
            link = job_links.nth(index)
            job_url = self._href(link, page.url)
            job_name = self._text(link)
            if (
                not job_url
                or not job_name
                or any(pattern in job_url.lower() for pattern in excluded_patterns)
                or any(pattern in job_name.lower() for pattern in excluded_patterns)
            ):
                continue

            location = "Remote"
            try:
                parent_lines = link.locator("xpath=..").inner_text().splitlines()
                location = next(
                    (
                        line.strip()
                        for line in parent_lines
                        if line.strip() and line.strip() != job_name and len(line.strip()) < 100
                    ),
                    location,
                )
            except PlaywrightError:
                pass

            result.append(
                {
                    "company": company,
                    "title": job_name,
                    "location": location,
                    "link": job_url,
                }
            )

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
