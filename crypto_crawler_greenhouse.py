from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner

jobs_file = 'crypto_jobs_greenhouse.json'
current_jobs_file = 'crypto_current_gh.json'

filtered_companies = Companies.filter_companies(category="crypto", scraper_type=Scrapers.GREENHOUSE)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
