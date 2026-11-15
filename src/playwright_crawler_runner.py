import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from queue import Empty, Queue

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
        if not isinstance(max_workers, int) or isinstance(max_workers, bool) or max_workers < 1:
            raise ValueError("max_workers must be a positive integer")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.jobs_file = jobs_file
        self.current_jobs_file = current_jobs_file
        self.headless = headless
        self.max_workers = max_workers
        self.max_attempts = max_attempts
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

    def _scrape_company(self, browser: Browser, company: CompanyItem, progress_info: str) -> list[dict]:
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

        if not jobs_data:
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
        return jobs_data

    def _write_results(self, company: CompanyItem, jobs_data: list[dict]) -> None:
        if jobs_data:
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
                    "date": str(datetime.date(datetime.now())),
                },
            )

    def _run_parallel(self, companies: list[CompanyItem]) -> None:
        tasks: Queue[tuple[int, CompanyItem]] = Queue()
        results: Queue[tuple[int, list[dict]] | BaseException] = Queue()
        stop = threading.Event()
        for index, company in enumerate(companies):
            tasks.put((index, company))

        def worker() -> None:
            try:
                with sync_playwright() as playwright:
                    browser = self._launch_browser(playwright)
                    try:
                        while not stop.is_set():
                            try:
                                index, company = tasks.get_nowait()
                            except Empty:
                                break
                            progress_info = f"scrape {index + 1} of {len(companies)}"
                            jobs_data = self._scrape_company(browser, company, progress_info)
                            results.put((index, jobs_data))
                    finally:
                        browser.close()
            except BaseException as error:
                stop.set()
                results.put(error)
                raise

        worker_count = min(self.max_workers, len(companies))
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            workers = [executor.submit(worker) for _ in range(worker_count)]
            try:
                pending: dict[int, list[dict]] = {}
                next_index = 0
                for _ in companies:
                    result = results.get()
                    if isinstance(result, BaseException):
                        raise result
                    index, jobs_data = result
                    pending[index] = jobs_data
                    while next_index in pending:
                        self._write_results(companies[next_index], pending.pop(next_index))
                        next_index += 1
                for worker_result in workers:
                    worker_result.result()
            finally:
                stop.set()

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

        if self.max_workers > 1 and companies:
            self._run_parallel(companies)
        else:
            with sync_playwright() as playwright:
                browser = self._launch_browser(playwright)
                try:
                    for index, company in enumerate(companies, start=1):
                        progress_info = f"scrape {index} of {len(companies)}"
                        jobs_data = self._scrape_company(browser, company, progress_info)
                        self._write_results(company, jobs_data)
                finally:
                    browser.close()

        self.logger.info(
            "Crawler run complete",
            extra={"duration_minutes": round((time.time() - start_time) / 60, 2)},
        )
