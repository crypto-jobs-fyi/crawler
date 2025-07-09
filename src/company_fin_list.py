import json
from typing import Any

from src.scrape_lever import ScrapeLever
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_greenhouse import ScrapeGreenhouse


def get_company_list() -> list[CompanyItem | Any]:
    return [
        CompanyItem('flex', 'https://job-boards.greenhouse.io/flex', ScrapeGreenhouse, 'https://getflex.com'),
        CompanyItem('Box', 'https://job-boards.greenhouse.io/boxinc', ScrapeGreenhouse, 'https://www.box.com'),
        CompanyItem('Aven', 'https://jobs.ashbyhq.com/Aven', ScrapeAshbyhq, 'https://www.aven.com'),
        CompanyItem('Ivy', 'https://jobs.ashbyhq.com/get-ivy', ScrapeAshbyhq, 'https://www.getivy.io'),
        CompanyItem("moneybox", "https://jobs.lever.co/moneyboxapp", ScrapeLever, "https://www.moneyboxapp.com"),
        
    ]


def get_company(name) -> CompanyItem:
    company_list = get_company_list()
    companies = list(filter(lambda jd: jd.company_name == name, company_list))
    if len(companies) > 1:
        raise NameError(f'Duplicated company name: {name}')
    return companies[0]


def write_companies(file_name):
    result_list = []
    for com in get_company_list():
        company_item = {
            "company_name": com.company_name,
            "company_url": com.company_url,
            "jobs_url": com.jobs_url,
        }
        result_list.append(company_item)
    print(f'[COMPANY_LIST] Number of Companies writen {len(result_list)}')
    with open(file_name, 'w') as companies_file:
        json.dump(result_list, companies_file, indent=4)
