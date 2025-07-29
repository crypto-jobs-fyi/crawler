import json

from src.scrape_lever import ScrapeLever
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_greenhouse import ScrapeGreenhouse


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem('life360', 'https://job-boards.greenhouse.io/life360', ScrapeGreenhouse, 'https://www.life360.com'),
        CompanyItem("kong", "https://jobs.lever.co/kong", ScrapeLever, "https://www.konghq.com"),
        CompanyItem("snaplogic", "https://jobs.lever.co/snaplogic", ScrapeLever, "https://www.snaplogic.com"),
        CompanyItem('runpod', 'https://job-boards.greenhouse.io/runpod', ScrapeGreenhouse, 'https://runpod.io'),
        CompanyItem('tenable', 'https://job-boards.greenhouse.io/tenableinc', ScrapeGreenhouse, 'https://www.tenable.com'),
        CompanyItem('veeam', 'https://job-boards.eu.greenhouse.io/veeamsoftware', ScrapeGreenhouse, 'https://www.veeam.com'),

        CompanyItem("n8n", "https://jobs.ashbyhq.com/n8n", ScrapeAshbyhq, "https://n8n.io"),
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
