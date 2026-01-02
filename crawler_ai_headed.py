import tempfile

from src.companies import Companies
from src.company_ai_list import get_company_list
from src.crawler_runner import CrawlerRunner


user_data_dir = tempfile.mkdtemp()  # Creates a unique temp directory
jobs_file = 'headed_ai_jobs.json'
current_jobs_file = 'headed_ai_current_jobs.json'

company_list = get_company_list()
filtered_companies = Companies.filter_companies_by_name(company_list, ['Cleo'])

runner = CrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)

