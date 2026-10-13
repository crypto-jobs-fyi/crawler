from src.companies import Companies
from src.playwright_crawler_runner import PlaywrightCrawlerRunner
from src.scrape_avara import ScrapeAvara
from src.scrape_coinbase import ScrapeCoinbase
from src.scrape_kula import ScrapeKula
from src.scrape_robinhood import ScrapeRobinhood
from src.scrape_sygnum import ScrapeSygnum


jobs_file = 'headed_crypto_jobs.json'
current_jobs_file = 'headed_crypto_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="crypto", company_names=['coinbase', 'sygnum', 'paradigm.co', 'avara', 'robinhood'])

playwright_scrapers = {
    "coinbase": ScrapeCoinbase,
    "sygnum": ScrapeSygnum,
    "paradigm.co": ScrapeKula,
    "avara": ScrapeAvara,
    "robinhood": ScrapeRobinhood,
}

for company in filtered_companies:
    company.scraper_type = playwright_scrapers[company.company_name]

runner = PlaywrightCrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)
