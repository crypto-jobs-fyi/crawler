from src.company_item import CompanyItem
from src.company_tech_list import get_company_list
from src.companies import Companies
from src.crawler_runner import CrawlerRunner


jobs_file = 'tech_jobs.json'
current_jobs_file = 'tech_current_jobs.json'
companies_file = 'tech_companies.json'

company_list: list[CompanyItem] = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
Companies.write_companies(companies_file, company_list)

# No exclusion as requested
filtered_companies = company_list

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)

