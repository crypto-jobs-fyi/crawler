from enum import Enum

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