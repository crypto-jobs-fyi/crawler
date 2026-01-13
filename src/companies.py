import json


from src.company_item import CompanyItem
from src.scrapers import Scrapers
from src.logging_utils import get_logger

logger = get_logger(__name__)

class Companies:
    _cached_companies: list[CompanyItem] = None

    @staticmethod
    def load_companies() -> list[CompanyItem]:
        if Companies._cached_companies is not None:
             return Companies._cached_companies
             
        try:
            with open('companies.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            logger.error("companies.json not found")
            return []
        
        companies = []
        company_list_raw = config.get('companies', []) if isinstance(config, dict) else config
        
        for c in company_list_raw:
             scraper_name = c.get('scraper')
             scraper_type = getattr(Scrapers, scraper_name) if scraper_name else None
             
             companies.append(CompanyItem(
                 company_name=c.get('name', c.get('company_name')),
                 jobs_url=c.get('jobs_url'),
                 scraper_type=scraper_type,
                 company_url=c.get('company_url'),
                 category=c.get('category'),
                 enabled=c.get('enabled', True),
                 headless=c.get('headless', True)
             ))
        
        Companies._cached_companies = companies
        return companies

    @staticmethod
    def get_company(name: str, company_list: list[CompanyItem] = None) -> CompanyItem:
        if company_list is None:
            company_list = Companies.load_companies()
        companies = list(filter(lambda jd: jd.company_name == name, company_list))
        if len(companies) > 1:
            raise NameError(f'Duplicated company name: {name}')
        return companies[0]

    @staticmethod
    def filter_companies(category: str = None, scraper_type = None) -> list[CompanyItem]:
        companies = Companies.load_companies()
        filtered = [c for c in companies if c.enabled]
        if category:
            filtered = [c for c in filtered if c.category == category]
        if scraper_type:
            filtered = [c for c in filtered if c.scraper_type == scraper_type]
        return filtered
    
    @staticmethod
    def filter_companies_not(category: str = None, scraper_types: list = None) -> list[CompanyItem]:
        companies = Companies.load_companies()
        filtered = [c for c in companies if c.enabled]
        if category:
            filtered = [c for c in filtered if c.category == category]
        if scraper_types:
            filtered = [company for company in filtered if getattr(company, 'scraper_type', None) not in scraper_types]
        return filtered

    @staticmethod
    def filter_companies_by_name(category: str = None, company_names: list[str] = None) -> list[CompanyItem]:
        companies = Companies.load_companies()
        filtered = [c for c in companies if c.enabled]
        if category:
            filtered = [c for c in filtered if c.category == category]
        if company_names:
            filtered = [company for company in filtered if company.company_name in company_names]
        return filtered
