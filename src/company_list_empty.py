from src.company_item import CompanyItem
from src.scrapers import Scrapers


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem("archblock", "https://jobs.lever.co/archblock", Scrapers.LEVER, "https://www.archblock.com"),
        CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', Scrapers.WORKABLE,
                    'https://smarttokenlabs.com'),
        CompanyItem("request", "https://jobs.lever.co/request", Scrapers.LEVER, "https://request.network"),
        CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', Scrapers.LEVER, 'https://www.blockswap.network'),
        CompanyItem('ultra', 'https://jobs.lever.co/ultra', Scrapers.LEVER, 'https://ultra.io'),
        CompanyItem('glassnode', 'https://jobs.lever.co/glassnode', Scrapers.LEVER, 'https://glassnode.com'),
        CompanyItem('Boost', 'https://jobs.ashbyhq.com/Boost', Scrapers.ASHBYHQ, 'https://Boost.xyz'),
        CompanyItem('pyth', 'https://jobs.ashbyhq.com/pythnetwork', Scrapers.GREENHOUSE,
                    'https://pyth.network'),
        CompanyItem("autonomys.xyz", "https://jobs.lever.co/autonomys", Scrapers.LEVER,
                    "https://www.autonomys.xyz"),
        CompanyItem("biconomy", "https://jobs.ashbyhq.com/biconomy", Scrapers.ASHBYHQ, "https://www.biconomy.io"),
        CompanyItem('goldsky', 'https://jobs.ashbyhq.com/goldsky', Scrapers.ASHBYHQ,
                    'https://goldsky.com'),
        CompanyItem('filecoinfoundation', "https://boards.greenhouse.io/filecoinfoundation", Scrapers.GREENHOUSE,
                    "https://fil.org"),
        CompanyItem('econetwork', 'https://job-boards.greenhouse.io/ecoinc', Scrapers.GREENHOUSE,
                    'https://eco.com'),
        CompanyItem('obol-tech', 'https://jobs.lever.co/obol-tech', Scrapers.LEVER, 'https://obol.tech'),
        CompanyItem("coinlist", "https://apply.workable.com/coinlist", Scrapers.WORKABLE, "https://coinlist.co"),
        CompanyItem('distributedcrafts', 'https://apply.workable.com/distributedcrafts', Scrapers.WORKABLE,
                    'https://www.gobob.xyz/'),
        CompanyItem('prepo', 'https://apply.workable.com/prepo', Scrapers.WORKABLE,
                    'https://prepo.io'),
        CompanyItem("nimbus", "https://job-boards.greenhouse.io/nimbus", Scrapers.GREENHOUSE,
                    "https://free.technology/nimbus"),
        CompanyItem("messari", "https://boards.greenhouse.io/messari", Scrapers.GREENHOUSE, "https://messari.io"),
        CompanyItem('shadow', 'https://jobs.ashbyhq.com/shadow', Scrapers.ASHBYHQ,
                    'https://www.shadow.xyz'),
        CompanyItem('flipsidecrypto', 'https://jobs.ashbyhq.com/flipsidecrypto', Scrapers.ASHBYHQ, 'https://flipsidecrypto.xyz'),
        CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', Scrapers.LEVER, 'https://multiversx.com'),
    ]
