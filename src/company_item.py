from dataclasses import dataclass
from src.scrape_it import ScrapeIt


@dataclass(init=True)
class CompanyItem:
    company_name: str
    jobs_url: str
    scraper_type: type[ScrapeIt]
    company_url: str
    category: str = None
    enabled: bool = True
    headless: bool = True
