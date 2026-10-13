from src.scrapers import Scrapers
from src.companies import Companies
from src.playwright_crawler_runner import PlaywrightCrawlerRunner


jobs_file = 'fin_jobs_greenhouse.json'
current_jobs_file = 'fin_current_jobs_greenhouse.json'

filtered_companies = Companies.filter_companies(
    category="fintech",
    scraper_type=Scrapers.GREENHOUSE,
)

runner = PlaywrightCrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
