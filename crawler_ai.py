from src.scrapers import Scrapers
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

jobs_file = 'ai_jobs.json'
current_jobs_file = 'ai_current_jobs.json'

logger = get_logger(__name__)

exclude = [Scrapers.ASHBYHQ, Scrapers.GREENHOUSE, Scrapers.LEVER]
filtered_companies = Companies.filter_companies_not(category="ai", scraper_types=exclude)

logger.info(
    "Companies loaded",
    extra={"company_count": len(filtered_companies), "jobs_file": jobs_file},
)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
