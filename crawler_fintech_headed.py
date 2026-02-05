from src.companies import Companies
from src.crawler_runner import CrawlerRunner


jobs_file = 'headed_fintech_jobs.json'
current_jobs_file = 'headed_fintech_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="fintech", company_names=['huspy', 'Cleo'])

runner = CrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)
