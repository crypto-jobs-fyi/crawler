from selenium import webdriver
from src.company_item import CompanyItem
from src.companies import Companies
from src.scrape_it import ScrapeIt
from src.company_list import get_company_list as crypto_company_list
from src.company_ai_list import get_company_list as ai_company_list

company_list = crypto_company_list() + ai_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
company_name_list = ['enjins']

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options=chrome_options)


for company_name in company_name_list:
    company: CompanyItem = Companies.get_company(company_name, company_list)
    crawler_type: ScrapeIt = company.scraper_type()
    jobs_data = crawler_type.getJobs(driver, company.jobs_url, company_name)
    ScrapeIt.write_jobs(jobs_data)

driver.close()
