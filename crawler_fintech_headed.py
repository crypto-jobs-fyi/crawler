from src.companies import Companies
from src.playwright_crawler_runner import PlaywrightCrawlerRunner
from src.scrape_revolut_people import ScrapeRevolutPeople


jobs_file = 'headed_fintech_jobs.json'
current_jobs_file = 'headed_fintech_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(
    category="fintech",
    company_names=["huspy", "revolut"],
)

for company in filtered_companies:
    if company.company_name == "huspy":
        company.scraper_type = ScrapeRevolutPeople

runner = PlaywrightCrawlerRunner(
    jobs_file,
    current_jobs_file,
    headless=False,
    max_attempts=2,
)
runner.run(filtered_companies)
