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
        CompanyItem("tessera", "https://jobs.lever.co/ftc", ScrapeLever, "https://tessera.co", "NFT"),
        CompanyItem("moonwalk", "https://boards.greenhouse.io/moonwalk", ScrapeGreenhouse,
                    "https://www.moonwalk.com", "Platform"),
        CompanyItem("tron", "https://boards.greenhouse.io/rainberry", ScrapeGreenhouse, "https://tron.network",
                    "Blockchain"),
        CompanyItem("jumpcrypto", "https://boards.greenhouse.io/jumpcrypto", ScrapeGreenhouse,
                    "https://jumpcrypto.com", "Infra"),
        CompanyItem("poap", "https://boards.greenhouse.io/poaptheproofofattendanceprotocol", ScrapeGreenhouse,
                    "https://poap.xyz", "Protocol"),
        CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', ScrapeWorkable,
                    'https://smarttokenlabs.com', 'Web3 bridge'),
        CompanyItem('avantgarde', 'https://apply.workable.com/avantgarde', ScrapeWorkable,
                    'https://avantgarde.finance', 'Asset Management'),
        CompanyItem('stably', 'https://apply.workable.com/stably', ScrapeWorkable, 'https://stably.io',
                    'Stable Coin'),
        CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                    'https://www.iofinnet.com', 'Custody'),
        CompanyItem("amun", "https://boards.greenhouse.io/amun", ScrapeGreenhouse, "https://amun.com", "DeFi"),
        CompanyItem('almanak', 'https://apply.workable.com/almanak-blockchain-labs-ag', ScrapeWorkable,
                    'https://almanak.co', 'Web3 Simulator'),
        CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhq, 'https://dune.com',
                    'Web3 data'),
        CompanyItem('outlierventures', 'https://boards.eu.greenhouse.io/outlierventures', ScrapeGreenhouse,
                    'https://outlierventures.io', 'Web3 Ventures'),
        CompanyItem('thetie', 'https://apply.workable.com/thetie', ScrapeWorkable,
                    'https://www.thetie.io', 'Web3 DeFi Info'),
        CompanyItem('dydxopsdao', 'https://apply.workable.com/dydx-operations-trust', ScrapeWorkable,
                    'https://dydxopsdao.com', 'Web3 DAO')
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
