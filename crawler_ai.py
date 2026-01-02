from src.scrapers import Scrapers
from src.company_item import CompanyItem
from src.company_ai_list import get_company_list
from src.companies import Companies
from src.crawler_runner import CrawlerRunner

jobs_file = 'ai_jobs.json'
current_jobs_file = 'ai_current_jobs.json'

company_list: list[CompanyItem] = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')

exclude = [Scrapers.ASHBYHQ, Scrapers.GREENHOUSE, Scrapers.LEVER]
filtered_companies = Companies.filter_companies_not(company_list, exclude)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
