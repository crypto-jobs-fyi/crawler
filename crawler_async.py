from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhqAsync
from src.scrape_lever import ScrapeLeverAsync
import time
from caqui import synchronous
import asyncio

MAX_CONCURRENCY = 5  # number of WebDriver instances
sem = asyncio.Semaphore(MAX_CONCURRENCY)


async def __schedule_tasks(companies):
    tasks = [asyncio.ensure_future(__collect_data(company)) for company in companies]
    await asyncio.gather(*tasks)


async def __collect_data(company):
    async with sem:
        driver_url = "http://127.0.0.1:9515"
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

        data = await company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
        for entry in data:
            print(entry)

        synchronous.close_session(*driver)


async def __schedule_tasks():
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
                    'https://ellipsislabs.xyz', 'Trading Protocol'),
        CompanyItem('bebop', 'https://jobs.lever.co/Bebop', ScrapeLeverAsync, 'https://bebop.xyz', 'DeFi Exchange'),
        CompanyItem("kraken", "https://jobs.lever.co/kraken", ScrapeLeverAsync, "https://kraken.com", "Exchange"),
        CompanyItem('arbitrumfoundation', 'https://jobs.lever.co/arbitrumfoundation', ScrapeLeverAsync,
                    'https://arbitrum.foundation', 'Layer 2'),
        CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLeverAsync, "https://chain.link",
                    "Blockchain"),
        CompanyItem("Polygon", "https://jobs.lever.co/Polygon", ScrapeLeverAsync, "https://polygon.technology",
                    "Blockchain"),
        CompanyItem("tokenmetrics", "https://jobs.lever.co/tokenmetrics", ScrapeLeverAsync,
                    "https://www.tokenmetrics.com", "Information"),
        CompanyItem("offchainlabs", "https://jobs.lever.co/offchainlabs", ScrapeLeverAsync,
                    "https://offchainlabs.com", "Protocol"),
        CompanyItem("subspacelabs", "https://jobs.lever.co/subspacelabs", ScrapeLeverAsync,
                    "https://subspace.network", "Blockchain Infra"),
        CompanyItem("ramp.network", "https://jobs.lever.co/careers.ramp.network", ScrapeLeverAsync,
                    "https://ramp.network", "Payments"),
        CompanyItem('risklabs', 'https://jobs.lever.co/risklabs', ScrapeLeverAsync, 'https://risklabs.foundation',
                    'Protocol'),
        CompanyItem('celestia', 'https://jobs.lever.co/celestia', ScrapeLeverAsync, 'https://celestia.org',
                    'Modular Blockchain'),
        CompanyItem('polymerlabs', 'https://jobs.lever.co/polymerlabs', ScrapeLeverAsync, 'https://www.polymerlabs.org',
                    'Modular Blockchain'),
        CompanyItem('royal', 'https://jobs.lever.co/Royal', ScrapeLeverAsync, 'https://royal.io', 'Web3 + Music'),
        CompanyItem('gauntlet', 'https://jobs.lever.co/gauntlet', ScrapeLeverAsync, 'https://gauntlet.network',
                    'Web3 + Financial Modelling'),
        CompanyItem("ledger", "https://jobs.lever.co/ledger", ScrapeLeverAsync, "https://www.ledger.com", "Wallet"),
        CompanyItem("request", "https://jobs.lever.co/request", ScrapeLeverAsync, "https://request.network",
                    "Payments"),
        CompanyItem('rain', 'https://jobs.ashbyhq.com/rain', ScrapeAshbyhqAsync, 'https://www.raincards.xyz',
                    'Web3 cards'),
        CompanyItem('exponential', 'https://jobs.ashbyhq.com/exponential', ScrapeAshbyhqAsync, 'https://exponential.fi',
                    'DeFi'),
    ]
    tasks = [asyncio.ensure_future(__collect_data(company)) for company in companies]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(__schedule_tasks())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        end = time.time()
        print(f"Time: {end - start:.2f} sec")
