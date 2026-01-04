import time
import threading
from queue import Queue, Empty
from datetime import datetime
from selenium import webdriver
from src.scrape_it import ScrapeIt
from src.company_item import CompanyItem

class CrawlerRunner:
    def __init__(self, jobs_file: str, current_jobs_file: str, headless: bool = True, max_workers: int = 2):
        self.jobs_file = jobs_file
        self.current_jobs_file = current_jobs_file
        self.headless = headless
        self.max_workers = max_workers
        self._initialize_files()
        self.file_lock = threading.Lock()

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
        print(f'[CRAWLER] {progress_info}')
        
        jobs_data = []
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                crawler_type: ScrapeIt = company.scraper_type()
                jobs_data = crawler_type.getJobs(driver, company.jobs_url, company.company_name)
                
                if len(jobs_data) > 0:
                    break
                
                if attempt < max_retries:
                    print(f'[CRAWLER] Company {company.company_name} returned 0 jobs. Retrying ({attempt + 1}/{max_retries})...')
                    time.sleep(2)
                    
            except Exception as e:
                print(f'[CRAWLER] Error processing {company.company_name}: {str(e)}')
                if attempt < max_retries:
                    print(f'[CRAWLER] Retrying ({attempt + 1}/{max_retries})...')
                    time.sleep(2)
        
        now = datetime.date(datetime.now())
        if jobs_data:
            with self.file_lock:
                ScrapeIt.write_jobs(jobs_data, self.jobs_file)
                ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), self.current_jobs_file)
            print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
        else:
            print(f'[CRAWLER] Company {company.company_name} failed to process or has 0 jobs after retries...')
        
        print(f'[CRAWLER] {company.company_name} Execution time:', round(time.time() - st), 'seconds')

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
        print(f'[CRAWLER] Starting scrape for {len(companies)} companies')

        if self.headless and self.max_workers > 1:
            q = Queue()
            for i, company in enumerate(companies):
                q.put((company, i + 1))
            
            threads = []
            num_workers = min(self.max_workers, len(companies))
            print(f'[CRAWLER] Running in parallel with {num_workers} workers')
            
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

        print('[CRAWLER] Total execution time:', round((time.time() - start_time)/60), 'minutes')
