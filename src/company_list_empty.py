import json

from src.company_item import CompanyItem
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
        CompanyItem('dappradar', 'https://dappradar.bamboohr.com/careers', ScrapeBamboohr,
                    'https://dappradar.com', 'Exchange & NFT'),
        CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                    'https://www.iofinnet.com', 'Custody'),
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
