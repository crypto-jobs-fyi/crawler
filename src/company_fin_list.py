from src.scrapers import Scrapers
from src.company_item import CompanyItem


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem('flex', 'https://job-boards.greenhouse.io/flex', Scrapers.GREENHOUSE.value, 'https://getflex.com'),
        CompanyItem('Box', 'https://job-boards.greenhouse.io/boxinc', Scrapers.GREENHOUSE.value, 'https://www.box.com'),
        CompanyItem('Aven', 'https://jobs.ashbyhq.com/Aven', Scrapers.ASHBYHQ.value, 'https://www.aven.com'),
        CompanyItem('Ivy', 'https://jobs.ashbyhq.com/get-ivy', Scrapers.ASHBYHQ.value, 'https://www.getivy.io'),
        CompanyItem("moneybox", "https://jobs.lever.co/moneyboxapp", Scrapers.LEVER.value, "https://www.moneyboxapp.com"),
        CompanyItem("affirm", "https://job-boards.greenhouse.io/affirm", Scrapers.GREENHOUSE.value, "https://www.affirm.com"),
        CompanyItem("huspy", "https://job-boards.greenhouse.io/huspy", Scrapers.GREENHOUSE.value, "https://www.huspy.com"),
        CompanyItem("paxos", "https://www.paxos.com/jobs", Scrapers.PAXOS.value, "https://www.paxos.com"),
        CompanyItem("circle", "https://careers.circle.com/us/en/search-results", Scrapers.CIRCLE.value, "https://www.circle.com"),
        CompanyItem("robinhood", "https://careers.robinhood.com", Scrapers.ROBINHOOD.value, "https://www.robinhood.com"),
        CompanyItem("qonto", "https://jobs.lever.co/qonto", Scrapers.LEVER.value, "https://www.qonto.com"),
        CompanyItem("ninjatrader", "https://job-boards.greenhouse.io/ninjatrader", Scrapers.GREENHOUSE.value, "https://www.ninjatrader.com"),
    ]
