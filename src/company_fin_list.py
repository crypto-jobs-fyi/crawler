from src.scrapers import Scrapers
from src.company_item import CompanyItem


def get_company_list() -> list[CompanyItem]:
    return [
        CompanyItem('flex', 'https://job-boards.greenhouse.io/flex', Scrapers.GREENHOUSE, 'https://getflex.com'),
        CompanyItem('Aven', 'https://jobs.ashbyhq.com/Aven', Scrapers.ASHBYHQ, 'https://www.aven.com'),
        CompanyItem('Ivy', 'https://jobs.ashbyhq.com/get-ivy', Scrapers.ASHBYHQ, 'https://www.getivy.io'),
        CompanyItem("qonto", "https://jobs.lever.co/qonto", Scrapers.LEVER, "https://www.qonto.com"),
        CompanyItem("moneybox", "https://jobs.lever.co/moneyboxapp", Scrapers.LEVER, "https://www.moneyboxapp.com"),
        CompanyItem("affirm", "https://job-boards.greenhouse.io/affirm", Scrapers.GREENHOUSE, "https://www.affirm.com"),
        CompanyItem("huspy", "https://job-boards.greenhouse.io/huspy", Scrapers.GREENHOUSE, "https://www.huspy.com"),
        CompanyItem("momentmarkets", "https://job-boards.greenhouse.io/momentmarkets", Scrapers.GREENHOUSE, "https://www.moment.com"),
        CompanyItem('9fin', 'https://jobs.ashbyhq.com/9fin', Scrapers.ASHBYHQ, 'https://www.9fin.com'),
        CompanyItem('grape-health', 'https://jobs.eu.lever.co/grape-health', Scrapers.LEVER, 'https://www.grapehealth.ch'),
        CompanyItem('cmgx', 'https://jobs.lever.co/cmgx', Scrapers.LEVER, 'https://www.cmgx.io'),
        CompanyItem("addepar", "https://job-boards.greenhouse.io/addepar1", Scrapers.GREENHOUSE, "https://addepar.com"),
        CompanyItem("clearstreet", "https://job-boards.greenhouse.io/clearstreet", Scrapers.GREENHOUSE, "https://clearstreet.io"),
        CompanyItem('onepay.com', 'https://jobs.ashbyhq.com/oneapp', Scrapers.ASHBYHQ, 'https://www.onepay.com'),
        CompanyItem("yuno", "https://jobs.lever.co/yuno", Scrapers.LEVER, "https://y.uno"),
        CompanyItem("capital", "https://jobs.lever.co/capital", Scrapers.LEVER, "https://www.capital.com"),
        CompanyItem("smartasset", "https://job-boards.greenhouse.io/smartasset", Scrapers.GREENHOUSE, "https://www.smartasset.com"),
        CompanyItem("earnin", "https://job-boards.greenhouse.io/earnin", Scrapers.GREENHOUSE, "https://www.earnin.com"),
        CompanyItem("getrecharge.com", "https://job-boards.greenhouse.io/recharge", Scrapers.GREENHOUSE, "https://getrecharge.com"),
    ]