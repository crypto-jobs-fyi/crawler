import tempfile

from src.companies import Companies
from src.crawler_runner import CrawlerRunner


user_data_dir = tempfile.mkdtemp()  # Creates a unique temp directory
jobs_file = 'headed_crypto_jobs.json'
current_jobs_file = 'headed_crypto_current_jobs.json'

filtered_companies = Companies.filter_companies_by_name(category="crypto", company_names=['coinbase', 'sygnum', 'paradigm.co', 'avara'])

runner = CrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)

