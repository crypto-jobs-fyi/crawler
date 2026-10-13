from src.companies import Companies
from src.playwright_crawler_runner import PlaywrightCrawlerRunner
from src.playwright_scrape_avara import ScrapeAvaraPlaywright
from src.playwright_scrape_coinbase import ScrapeCoinbasePlaywright
from src.playwright_scrape_kula import ScrapeKulaPlaywright
from src.playwright_scrape_robinhood import ScrapeRobinhoodPlaywright
from src.playwright_scrape_sygnum import ScrapeSygnumPlaywright


jobs_file = 'headed_crypto_jobs.json'
current_jobs_file = 'headed_crypto_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="crypto", company_names=['coinbase', 'sygnum', 'paradigm.co', 'avara', 'robinhood'])

playwright_scrapers = {
    "coinbase": ScrapeCoinbasePlaywright,
    "sygnum": ScrapeSygnumPlaywright,
    "paradigm.co": ScrapeKulaPlaywright,
    "avara": ScrapeAvaraPlaywright,
    "robinhood": ScrapeRobinhoodPlaywright,
}

for company in filtered_companies:
    company.scraper_type = playwright_scrapers[company.company_name]

runner = PlaywrightCrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)
