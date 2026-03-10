from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

jobs_file = 'fin_jobs_mix.json'
current_jobs_file = 'fin_current_jobs_mix.json'

logger = get_logger(__name__)

exclude = [Scrapers.CLEO]
filtered_companies = Companies.filter_companies_not(category="fintech", scraper_types=exclude)

logger.info(
    "Companies loaded",
    extra={"company_count": len(filtered_companies), "jobs_file": jobs_file},
)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
