from src.companies import Companies
from src.crawler_runner import CrawlerRunner


jobs_file = 'headed_ai_jobs.json'
current_jobs_file = 'headed_ai_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="ai", company_names=['Cleo'])

runner = CrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)

