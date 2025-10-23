from src.scrapers import Scrapers
from src.company_item import CompanyItem


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem('flex', 'https://job-boards.greenhouse.io/flex', Scrapers.GREENHOUSE.value, 'https://getflex.com'),
        CompanyItem('Aven', 'https://jobs.ashbyhq.com/Aven', Scrapers.ASHBYHQ.value, 'https://www.aven.com'),
        CompanyItem('Ivy', 'https://jobs.ashbyhq.com/get-ivy', Scrapers.ASHBYHQ.value, 'https://www.getivy.io'),
        CompanyItem("qonto", "https://jobs.lever.co/qonto", Scrapers.LEVER.value, "https://www.qonto.com"),
        CompanyItem("moneybox", "https://jobs.lever.co/moneyboxapp", Scrapers.LEVER.value, "https://www.moneyboxapp.com"),
        CompanyItem("affirm", "https://job-boards.greenhouse.io/affirm", Scrapers.GREENHOUSE.value, "https://www.affirm.com"),
        CompanyItem("huspy", "https://job-boards.greenhouse.io/huspy", Scrapers.GREENHOUSE.value, "https://www.huspy.com"),
        CompanyItem("momentmarkets", "https://job-boards.greenhouse.io/momentmarkets", Scrapers.GREENHOUSE.value, "https://www.moment.com"),
        CompanyItem('9fin', 'https://jobs.ashbyhq.com/9fin', Scrapers.ASHBYHQ.value, 'https://www.9fin.com'),
    ]
