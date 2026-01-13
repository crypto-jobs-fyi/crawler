from src.companies import Companies
from src.crawler_runner import CrawlerRunner
from src.logging_utils import get_logger


jobs_file = 'fin_jobs.json'
current_jobs_file = 'fin_current_jobs.json'

logger = get_logger(__name__)

company_list = Companies.filter_companies(category="fintech")
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": jobs_file},
)

runner = CrawlerRunner(jobs_file, current_jobs_file)
runner.run(company_list)
