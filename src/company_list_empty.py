import json

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_bamboohr import ScrapeBamboohr
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_lever import ScrapeLever
from src.scrape_workable import ScrapeWorkable


def get_company_list() -> []:
    return [
        CompanyItem("archblock", "https://jobs.lever.co/archblock", ScrapeLever, "https://www.archblock.com",
                    "Stable Coin"),
        CompanyItem("moonwalk", "https://boards.greenhouse.io/moonwalk", ScrapeGreenhouse,
                    "https://www.moonwalk.com", "Platform"),
        CompanyItem("tron", "https://boards.greenhouse.io/rainberry", ScrapeGreenhouse, "https://tron.network",
                    "Blockchain"),
        CompanyItem("poap", "https://boards.greenhouse.io/poaptheproofofattendanceprotocol", ScrapeGreenhouse,
                    "https://poap.xyz", "Protocol"),
        CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', ScrapeWorkable,
                    'https://smarttokenlabs.com', 'Web3 bridge'),
        CompanyItem('avantgarde', 'https://apply.workable.com/avantgarde', ScrapeWorkable,
                    'https://avantgarde.finance', 'Asset Management'),
        CompanyItem('stably', 'https://apply.workable.com/stably', ScrapeWorkable, 'https://stably.io',
                    'Stable Coin'),
        CompanyItem('thetie', 'https://apply.workable.com/thetie', ScrapeWorkable,
                    'https://www.thetie.io', 'Web3 DeFi Info'),
        CompanyItem('dydxopsdao', 'https://apply.workable.com/dydx-operations-trust', ScrapeWorkable,
                    'https://dydxopsdao.com', 'Web3 DAO'),
        CompanyItem('bitget', 'https://apply.workable.com/bitget', ScrapeWorkable, 'https://www.bitget.com/en',
                    'Exchange'),
        CompanyItem("bitcoin", "https://www.bitcoin.com/jobs/#joblist", ScrapeGreenhouse,
                    "https://www.bitcoin.com", 'Exchange'),
        CompanyItem('superfluid', 'https://apply.workable.com/superfluid/#jobs', ScrapeWorkable,
                    'https://www.superfluid.finance', 'Web3'),
        CompanyItem('mina-foundation', 'https://apply.workable.com/mina-foundation', ScrapeWorkable,
                    'https://www.minafoundation.com', 'ZK blockchain'),
    ]


def get_company(name) -> CompanyItem:
    company_list = get_company_list()
    companies = list(filter(lambda jd: jd.company_name == name, company_list))
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
