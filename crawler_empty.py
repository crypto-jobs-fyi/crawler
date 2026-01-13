from src.company_item import CompanyItem
from src.company_list_empty import get_company_list
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger

jobs_file: str = 'crypto_jobs_empty.json'
current_jobs_file = 'current_jobs_empty.json'
companies_file = 'companies_empty.json'

logger = get_logger(__name__)

company_list: list[CompanyItem] = get_company_list()
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": jobs_file},
)
Companies.write_companies(companies_file, company_list)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(company_list)

