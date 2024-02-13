from selenium import webdriver
from src.company_list import get_company_list
from src.company_list import get_company

company_list = get_company_list()
company_name_list = ['coinbase', 'consensys']

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options=chrome_options)


for company_name in company_name_list:
    company = get_company(company_name)
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company_name)

driver.close()
