from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner

jobs_file = 'ai_jobs_lever.json'
current_jobs_file = 'ai_current_jobs_lever.json'

filtered_companies = Companies.filter_companies(category="ai", scraper_type=Scrapers.LEVER)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)

