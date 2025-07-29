from enum import Enum

from scrape_base import ScrapeBase
from scrape_coinbase import ScrapeCoinbase
from scrape_ripple import ScrapeRipple
from scrape_smartrecruiters import ScrapeSmartrecruiters
from scrape_workable import ScrapeWorkable
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_circle import ScrapeCircle
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_lever import ScrapeLever
from src.scrape_paxos import ScrapePaxos
from src.scrape_robinhood import ScrapeRobinhood

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