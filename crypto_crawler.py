from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

jobs_file = 'crypto_jobs.json'
current_jobs_file = 'crypto_current_jobs.json'

logger = get_logger(__name__)

exclude = [Scrapers.GREENHOUSE, Scrapers.LEVER, Scrapers.ASHBYHQ, Scrapers.COINBASE, Scrapers.SYGNUM, Scrapers.KULA]
filtered_companies = Companies.filter_companies_not(category="crypto", scraper_types=exclude)

logger.info(
    "Companies loaded",
    extra={"company_count": len(filtered_companies), "jobs_file": jobs_file},
)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
