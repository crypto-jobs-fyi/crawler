from src.scrapers import Scrapers
from src.companies import Companies
from src.company_item import CompanyItem
from src.company_ai_list import get_company_list
from src.crawler_runner import CrawlerRunner

company_list: list[CompanyItem] = get_company_list()
jobs_file = 'ai_jobs_lever.json'
current_jobs_file = 'ai_current_jobs_lever.json'

filtered_companies = Companies.filter_companies(company_list, Scrapers.LEVER)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)

