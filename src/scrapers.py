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
from src.scrape_sygnum import ScrapeSygnum
from src.scrape_lmax import ScrapeLmax
from src.scrape_nebius import ScrapeNebius
from src.scrape_applied_intuition import ScrapeAppliedIntuition
from src.scrape_cleo import ScrapeCleo
from src.scrape_c3 import ScrapeC3
from src.scrape_gem import ScrapeGem
from src.scrape_bitcoinsuisse import ScrapeBitcoinSuisse
from src.scrape_gemini import ScrapeGemini
from src.scrape_kula import ScrapeKula
from src.scrape_world import ScrapeWorld
from src.scrape_avara import ScrapeAvara

class Scrapers:
    ROBINHOOD = ScrapeRobinhood
    CIRCLE = ScrapeCircle
    PAXOS = ScrapePaxos
    GEMINI = ScrapeGemini
    SYGNUM = ScrapeSygnum
    LEVER = ScrapeLever
    ASHBYHQ = ScrapeAshbyhq
    GREENHOUSE = ScrapeGreenhouse
    SMARTRECRUITERS = ScrapeSmartrecruiters
    WORKABLE = ScrapeWorkable
    COINBASE = ScrapeCoinbase
    BASE = ScrapeBase
    RIPPLE = ScrapeRipple
    BAMBOOHR = ScrapeBamboohr
    LMAX = ScrapeLmax
    NEBIUS = ScrapeNebius
    APPLIED_INTUITION = ScrapeAppliedIntuition
    CLEO = ScrapeCleo
    C3 = ScrapeC3
    GEM = ScrapeGem
    BITCOINSUISSE = ScrapeBitcoinSuisse
    KULA = ScrapeKula
    WORLDCOIN = ScrapeWorld
    AVARA = ScrapeAvara