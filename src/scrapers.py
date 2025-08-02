from enum import Enum

from src.scrape_base import ScrapeBase
from src.scrape_coinbase import ScrapeCoinbase
from src.scrape_ripple import ScrapeRipple
from src.scrape_smartrecruiters import ScrapeSmartrecruiters
from src.scrape_workable import ScrapeWorkable
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_circle import ScrapeCircle
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_lever import ScrapeLever
from src.scrape_paxos import ScrapePaxos
from src.scrape_robinhood import ScrapeRobinhood
from src.scrape_bamboohr import ScrapeBamboohr

class Scrapers(Enum):
    ROBINHOOD = ScrapeRobinhood
    CIRCLE = ScrapeCircle
    PAXOS = ScrapePaxos
    LEVER = ScrapeLever
    ASHBYHQ = ScrapeAshbyhq
    GREENHOUSE = ScrapeGreenhouse
    SMARTRECRUITERS = ScrapeSmartrecruiters
    WORKABLE = ScrapeWorkable
    COINBASE = ScrapeCoinbase
    BASE = ScrapeBase
    RIPPLE = ScrapeRipple
    BAMBOOHR = ScrapeBamboohr
