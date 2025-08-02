import json

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_bamboohr import ScrapeBamboohr
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_lever import ScrapeLever
from src.scrape_workable import ScrapeWorkable


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem("archblock", "https://jobs.lever.co/archblock", ScrapeLever, "https://www.archblock.com"),
        CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', ScrapeWorkable,
                    'https://smarttokenlabs.com'),
        CompanyItem('superfluid', 'https://apply.workable.com/superfluid/#jobs', ScrapeWorkable,
                    'https://www.superfluid.finance'),
        CompanyItem("request", "https://jobs.lever.co/request", ScrapeLever, "https://request.network"),
        CompanyItem('mina-foundation', 'https://apply.workable.com/mina-foundation', ScrapeWorkable,
                    'https://www.minafoundation.com'),
        CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', ScrapeLever, 'https://www.blockswap.network'),
        CompanyItem('ultra', 'https://jobs.lever.co/ultra', ScrapeLever, 'https://ultra.io'),
        CompanyItem('glassnode', 'https://jobs.lever.co/glassnode', ScrapeLever, 'https://glassnode.com'),
        CompanyItem('dappradar', 'https://dappradar.bamboohr.com/careers', ScrapeBamboohr,
                    'https://dappradar.com'),
        CompanyItem('web3', 'https://web3.bamboohr.com/careers', ScrapeBamboohr, 'https://web3.foundation'),
        CompanyItem("kadena", "https://boards.greenhouse.io/kadenallc", ScrapeGreenhouse, "https://kadena.io"),
        CompanyItem('protocollabs', 'https://boards.greenhouse.io/protocollabs', ScrapeGreenhouse,
                    'https://protocol.ai/about'),
        CompanyItem('Boost', 'https://jobs.ashbyhq.com/Boost', ScrapeAshbyhq, 'https://Boost.xyz'),
        CompanyItem('exponential', 'https://jobs.ashbyhq.com/exponential', ScrapeAshbyhq, 'https://exponential.fi'),
        CompanyItem('pyth', 'https://jobs.ashbyhq.com/pythnetwork', ScrapeGreenhouse,
                    'https://pyth.network'),
        CompanyItem('outlierventures', 'https://outlierventures.bamboohr.com/careers', ScrapeBamboohr,
                    'https://outlierventures.io'),
        CompanyItem("subspacelabs", "https://jobs.lever.co/autonomys", ScrapeLever,
                    "https://www.autonomys.xyz"),
        CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLever, "https://www.biconomy.io"),
        CompanyItem('coinmetrics', 'https://boards.greenhouse.io/coinmetrics', ScrapeGreenhouse,
                    'https://coinmetrics.io'),
        CompanyItem('goldsky', 'https://boards.greenhouse.io/goldsky', ScrapeGreenhouse,
                    'https://goldsky.com'),
        CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                    'https://www.iofinnet.com'),
        CompanyItem("filecoinfoundation", "https://boards.greenhouse.io/filecoinfoundation", ScrapeGreenhouse,
                    "https://fil.org"),
        CompanyItem("solana", "https://job-boards.greenhouse.io/solana", ScrapeGreenhouse,
                    "https://solana.com"),
        CompanyItem('osmosisdex', 'https://boards.greenhouse.io/osmosisdex', ScrapeGreenhouse, 'https://osmosis.zone'),
        CompanyItem('movementlabs', 'https://jobs.ashbyhq.com/movementlabs', ScrapeAshbyhq,
                    'https://movementlabs.xyz'),
        CompanyItem('magic', 'https://job-boards.greenhouse.io/magic', ScrapeGreenhouse, 'https://magic.link'),
        CompanyItem('econetwork', 'https://job-boards.greenhouse.io/ecoinc', ScrapeGreenhouse,
                    'https://eco.com'),
        CompanyItem("ramp.network", "https://job-boards.eu.greenhouse.io/rampnetwork", ScrapeGreenhouse,
                    "https://ramp.network"),
        CompanyItem('obol-tech', 'https://jobs.lever.co/obol-tech', ScrapeLever, 'https://obol.tech'),
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
