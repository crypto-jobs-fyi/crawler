from src.scrapers import Scrapers
from src.company_item import CompanyItem
from src.company_ai_list import get_company_list
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

jobs_file = 'ai_jobs.json'
current_jobs_file = 'ai_current_jobs.json'

logger = get_logger(__name__)

company_list: list[CompanyItem] = get_company_list()
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": jobs_file},
)

exclude = [Scrapers.ASHBYHQ, Scrapers.GREENHOUSE, Scrapers.LEVER]
filtered_companies = Companies.filter_companies_not(company_list, exclude)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
