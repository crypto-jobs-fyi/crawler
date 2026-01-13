from src.company_item import CompanyItem
from src.company_tech_list import get_company_list
from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger


jobs_file = 'tech_jobs.json'
current_jobs_file = 'tech_current_jobs.json'
companies_file = 'tech_companies.json'

logger = get_logger(__name__)

company_list: list[CompanyItem] = get_company_list()
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": jobs_file},
)
Companies.write_companies(companies_file, company_list)

# No exclusion as requested
filtered_companies = company_list

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(filtered_companies)

