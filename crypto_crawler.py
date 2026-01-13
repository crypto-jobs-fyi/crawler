from src.scrapers import Scrapers
from src.companies import Companies
from src.company_item import CompanyItem
from src.company_list import get_company_list
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

company_list: list[CompanyItem] = get_company_list()
jobs_file = 'crypto_jobs.json'
current_jobs_file = 'crypto_current_jobs.json'

logger = get_logger(__name__)
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": jobs_file},
)

exclude = [Scrapers.GREENHOUSE, Scrapers.LEVER, Scrapers.ASHBYHQ, Scrapers.COINBASE, Scrapers.SYGNUM, Scrapers.KULA]
filtered_companies = Companies.filter_companies_not(company_list, exclude)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)
