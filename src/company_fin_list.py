import json
from typing import Any

from src.scrape_robinhood import ScrapeRobinhood
from src.scrape_circle import ScrapeCircle
from src.scrape_paxos import ScrapePaxos
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
        CompanyItem("affirm", "https://job-boards.greenhouse.io/affirm", ScrapeGreenhouse, "https://www.affirm.com"),
        CompanyItem("huspy", "https://job-boards.greenhouse.io/huspy", ScrapeGreenhouse, "https://www.huspy.com"),
        CompanyItem("paxos", "https://www.paxos.com/jobs", ScrapePaxos, "https://www.paxos.com"),
        CompanyItem("circle", "https://careers.circle.com/us/en/search-results", ScrapeCircle, "https://www.circle.com"),
        CompanyItem("robinhood", "https://careers.robinhood.com", ScrapeRobinhood, "https://www.robinhood.com"),
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
