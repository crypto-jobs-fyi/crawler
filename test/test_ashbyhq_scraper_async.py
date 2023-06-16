from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhqAsync
import time
from caqui import synchronous
from pytest import mark

@mark.asyncio
async def test_ashbyhq_async():
    start = time.time()
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "name": "webdriver",
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
            # uncomment to set headless
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    session = synchronous.get_session(driver_url, capabilities)
    driver = [driver_url, session]

    companies = [
        CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', ScrapeAshbyhqAsync, 'https://www.kiln.fi', 'Staking'),
        CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhqAsync, 'https://dune.com',
                    'Web3 data'),
        CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', ScrapeAshbyhqAsync, 'https://conduit.xyz',
                    'Infrastructure'),
        CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', ScrapeAshbyhqAsync, 'https://www.paradigm.xyz',
                    'Web3 data'),
        CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhqAsync, 'https://www.sygnum.com',
                    'Crypto bank'),
        CompanyItem('solana-foundation', 'https://jobs.ashbyhq.com/Solana%20Foundation', ScrapeAshbyhqAsync,
                    'https://www.sygnum.com',
                    'Crypto bank'),
        CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhqAsync,
                    'https://ellipsislabs.xyz', 'Trading Protocol')
    ]

    for company in companies:
        data = await company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
        for entry in data:
            print(entry)

    synchronous.close_session(*driver)

    end = time.time()
    print(f"Time: {end-start:.2f} sec")
