from src.company_item import CompanyItem
from src.scrapers import Scrapers


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem('life360', 'https://job-boards.greenhouse.io/life360', Scrapers.GREENHOUSE.value, 'https://www.life360.com'),
        CompanyItem("kong", "https://jobs.lever.co/kong", Scrapers.LEVER.value, "https://www.konghq.com"),
        CompanyItem("snaplogic", "https://jobs.lever.co/snaplogic", Scrapers.LEVER.value, "https://www.snaplogic.com"),
        CompanyItem('runpod', 'https://job-boards.greenhouse.io/runpod', Scrapers.GREENHOUSE.value, 'https://runpod.io'),
        CompanyItem('tenable', 'https://job-boards.greenhouse.io/tenableinc', Scrapers.GREENHOUSE.value, 'https://www.tenable.com'),
        CompanyItem('veeam', 'https://job-boards.eu.greenhouse.io/veeamsoftware', Scrapers.GREENHOUSE.value, 'https://www.veeam.com'),
    ]
