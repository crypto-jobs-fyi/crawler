import time
from datetime import datetime
from selenium import webdriver
from src.scrape_it import ScrapeIt
from src.company_item import CompanyItem

class CrawlerRunner:
    def __init__(self, jobs_file: str, current_jobs_file: str, headless: bool = True):
        self.jobs_file = jobs_file
        self.current_jobs_file = current_jobs_file
        self.headless = headless
        self._initialize_files()

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

    def run(self, companies: list[CompanyItem]):
        driver = self._get_driver()
        n = 1
        now = datetime.date(datetime.now())
        start_time = time.time()
        
        print(f'[CRAWLER] Starting scrape for {len(companies)} companies')

        for company in companies:
            st = time.time()
            print(f'[CRAWLER] scrape {n} of {len(companies)}')
            n += 1
            
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
            
            if jobs_data:
                ScrapeIt.write_jobs(jobs_data, self.jobs_file)
                ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), self.current_jobs_file)
                print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
            else:
                print(f'[CRAWLER] Company {company.company_name} failed to process or has 0 jobs after retries...')
            
            print('[CRAWLER] Execution time:', round(time.time() - st), 'seconds')

        print('[CRAWLER] Total execution time:', round((time.time() - start_time)/60), 'minutes')
        driver.close()
