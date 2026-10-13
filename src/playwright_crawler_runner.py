import threading
import time
from datetime import datetime

from playwright.sync_api import Browser, Page, sync_playwright

from src.company_item import CompanyItem
from src.logging_utils import get_logger
from src.playwright_adapter import PlaywrightPageAdapter
from src.scrape_it import ScrapeIt


class PlaywrightCrawlerRunner:
    def __init__(
        self,
        jobs_file: str,
        current_jobs_file: str,
        headless: bool = True,
        max_workers: int = 1,
        max_attempts: int = 3,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.jobs_file = jobs_file
        self.current_jobs_file = current_jobs_file
        self.headless = headless
        self.max_workers = max_workers
        self.max_attempts = max_attempts
        self.file_lock = threading.Lock()
        self.logger = get_logger(self.__class__.__name__)
        self._initialize_files()

    def _initialize_files(self) -> None:
        with open(self.jobs_file, "w") as jobs_file:
            jobs_file.write("{}")
        with open(self.current_jobs_file, "w") as current_jobs_file:
            current_jobs_file.write("{}")

    def _launch_browser(self, playwright) -> Browser:
        return playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"],
        )

    def _scrape_company(self, browser: Browser, company: CompanyItem, progress_info: str) -> None:
        started_at = time.time()
        self.logger.info(
            "Scrape start",
            extra={"progress": progress_info, "company": company.company_name},
        )
        jobs_data = []

        for attempt in range(self.max_attempts):
            context = browser.new_context()
            page: Page = context.new_page()
            try:
                crawler_type: ScrapeIt = company.scraper_type()
                jobs_data = crawler_type.getJobs(
                    PlaywrightPageAdapter(page),
                    company.jobs_url,
                    company.company_name,
                )
                if jobs_data:
                    break
                if attempt < self.max_attempts - 1:
                    self.logger.warning(
                        "No jobs returned",
                        extra={
                            "company": company.company_name,
                            "attempt": attempt + 1,
                            "max_attempts": self.max_attempts,
                        },
                    )
                    time.sleep(2)
            except Exception:
                self.logger.error(
                    "Scrape error",
                    exc_info=True,
                    extra={
                        "company": company.company_name,
                        "attempt": attempt + 1,
                        "max_attempts": self.max_attempts,
                    },
                )
                if attempt < self.max_attempts - 1:
                    self.logger.info(
                        "Retrying scrape",
                        extra={
                            "company": company.company_name,
                            "attempt": attempt + 1,
                            "max_attempts": self.max_attempts,
                        },
                    )
                    time.sleep(2)
            finally:
                context.close()

        today = datetime.date(datetime.now())
        if jobs_data:
            with self.file_lock:
                ScrapeIt.write_jobs(jobs_data, self.jobs_file)
                ScrapeIt.write_current_jobs_number(
                    company.company_name,
                    len(jobs_data),
                    self.current_jobs_file,
                )
            self.logger.info(
                "Scrape success",
                extra={
                    "company": company.company_name,
                    "job_count": len(jobs_data),
                    "date": str(today),
                },
            )
        else:
            self.logger.error(
                "Scrape failed",
                extra={
                    "company": company.company_name,
                    "attempts": self.max_attempts,
                },
            )

        self.logger.info(
            "Scrape complete",
            extra={
                "company": company.company_name,
                "duration_seconds": round(time.time() - started_at, 2),
            },
        )

    def run(self, companies: list[CompanyItem]) -> None:
        start_time = time.time()
        if self.headless:
            original_count = len(companies)
            companies = [company for company in companies if company.headless]
            skipped = original_count - len(companies)
            if skipped:
                self.logger.info(
                    "Skipping companies requiring headed mode",
                    extra={"skipped_count": skipped, "remaining_count": len(companies)},
                )

        self.logger.info(
            "Crawler run start",
            extra={
                "company_count": len(companies),
                "headless": self.headless,
                "max_workers": self.max_workers,
            },
        )

        with sync_playwright() as playwright:
            browser = self._launch_browser(playwright)
            try:
                for index, company in enumerate(companies, start=1):
                    progress_info = f"scrape {index} of {len(companies)}"
                    self._scrape_company(browser, company, progress_info)
            finally:
                browser.close()

        self.logger.info(
            "Crawler run complete",
            extra={"duration_minutes": round((time.time() - start_time) / 60, 2)},
        )
