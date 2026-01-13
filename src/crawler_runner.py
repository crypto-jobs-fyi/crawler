import time
import threading
from queue import Queue, Empty
from datetime import datetime
from selenium import webdriver
from src.scrape_it import ScrapeIt
from src.company_item import CompanyItem
from src.logging_utils import get_logger

class CrawlerRunner:
    def __init__(self, jobs_file: str, current_jobs_file: str, headless: bool = True, max_workers: int = 2):
        self.jobs_file = jobs_file
        self.current_jobs_file = current_jobs_file
        self.headless = headless
        self.max_workers = max_workers
        self._initialize_files()
        self.file_lock = threading.Lock()
        self.logger = get_logger(self.__class__.__name__)

    def _initialize_files(self):
        with open(self.jobs_file, 'w') as f:
            f.write('{}')
        with open(self.current_jobs_file, 'w') as cf:
            cf.write('{}')

    def _get_driver(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-extensions')
        return webdriver.Chrome(options=chrome_options)

    def _scrape_company(self, driver: webdriver.Chrome, company: CompanyItem, progress_info: str):
        st = time.time()
        self.logger.info("Scrape start", extra={"progress": progress_info, "company": company.company_name})
        
        jobs_data = []
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                crawler_type: ScrapeIt = company.scraper_type()
                jobs_data = crawler_type.getJobs(driver, company.jobs_url, company.company_name)
                
                if len(jobs_data) > 0:
                    break
                
                if attempt < max_retries:
                    self.logger.warning(
                        "No jobs returned",
                        extra={
                            "company": company.company_name,
                            "attempt": attempt + 1,
                            "max_attempts": max_retries + 1,
                        },
                    )
                    time.sleep(2)
                    
            except Exception as e:
                self.logger.error(
                    "Scrape error",
                    exc_info=True,
                    extra={
                        "company": company.company_name,
                        "attempt": attempt + 1,
                        "max_attempts": max_retries + 1,
                    },
                )
                if attempt < max_retries:
                    self.logger.info(
                        "Retrying scrape",
                        extra={
                            "company": company.company_name,
                            "attempt": attempt + 1,
                            "max_attempts": max_retries + 1,
                        },
                    )
                    time.sleep(2)
        
        now = datetime.date(datetime.now())
        if jobs_data:
            with self.file_lock:
                ScrapeIt.write_jobs(jobs_data, self.jobs_file)
                ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), self.current_jobs_file)
            self.logger.info(
                "Scrape success",
                extra={
                    "company": company.company_name,
                    "job_count": len(jobs_data),
                    "date": str(now),
                },
            )
        else:
            self.logger.error(
                "Scrape failed",
                extra={
                    "company": company.company_name,
                    "attempts": max_retries + 1,
                },
            )

        self.logger.info(
            "Scrape complete",
            extra={
                "company": company.company_name,
                "duration_seconds": round(time.time() - st, 2),
            },
        )

    def _worker(self, q: Queue, total_companies: int):
        driver = self._get_driver()
        try:
            while True:
                try:
                    item = q.get_nowait()
                except Empty:
                    break
                
                company, idx = item
                progress_info = f'scrape {idx} of {total_companies} ({company.company_name})'
                self._scrape_company(driver, company, progress_info)
                q.task_done()
        finally:
            driver.quit()

    def run(self, companies: list[CompanyItem]):
        start_time = time.time()
        self.logger.info(
            "Crawler run start",
            extra={"company_count": len(companies), "headless": self.headless, "max_workers": self.max_workers},
        )

        if self.headless and self.max_workers > 1:
            q = Queue()
            for i, company in enumerate(companies):
                q.put((company, i + 1))
            
            threads = []
            num_workers = min(self.max_workers, len(companies))
            self.logger.info(
                "Parallel execution",
                extra={"workers": num_workers, "headless": self.headless},
            )
            
            for _ in range(num_workers):
                t = threading.Thread(target=self._worker, args=(q, len(companies)))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
        else:
            driver = self._get_driver()
            try:
                n = 1
                for company in companies:
                    progress_info = f'scrape {n} of {len(companies)}'
                    self._scrape_company(driver, company, progress_info)
                    n += 1
            finally:
                driver.close()

        self.logger.info(
            "Crawler run complete",
            extra={"duration_minutes": round((time.time() - start_time) / 60, 2)},
        )
