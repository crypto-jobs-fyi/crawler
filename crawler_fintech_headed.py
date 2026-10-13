from src.companies import Companies
from src.playwright_crawler_runner import PlaywrightCrawlerRunner
from src.playwright_scrape_revolut_people import ScrapeRevolutPeoplePlaywright


jobs_file = 'headed_fintech_jobs.json'
current_jobs_file = 'headed_fintech_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="fintech", company_names=['huspy'])

for company in filtered_companies:
    company.scraper_type = ScrapeRevolutPeoplePlaywright

runner = PlaywrightCrawlerRunner(jobs_file, current_jobs_file, headless=True)
runner.run(filtered_companies)
