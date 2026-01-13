from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner

jobs_file = 'crypto_jobs_ashby.json'
current_jobs_file = 'crypto_current_ashby.json'

filtered_companies = Companies.filter_companies(category="crypto", scraper_type=Scrapers.ASHBYHQ)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
