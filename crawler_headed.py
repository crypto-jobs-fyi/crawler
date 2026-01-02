import tempfile
import time
from datetime import datetime

from selenium import webdriver

import tempfile
from src.scrapers import Scrapers
from src.company_item import CompanyItem
from src.scrape_it import ScrapeIt
from src.companies import Companies
from src.company_list import get_company_list
from src.crawler_runner import CrawlerRunner


user_data_dir = tempfile.mkdtemp()  # Creates a unique temp directory
jobs_file = 'headed_jobs.json'
current_jobs_file = 'headed_current_jobs.json'

company_list = get_company_list()
filtered_companies = Companies.filter_companies_by_name(company_list, ['coinbase', 'sygnum', 'paradigm.co', 'avara'])

runner = CrawlerRunner(jobs_file, current_jobs_file, headless=False)
runner.run(filtered_companies)

