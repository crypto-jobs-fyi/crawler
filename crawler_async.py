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
        CompanyItem('rain', 'https://jobs.ashbyhq.com/rain', ScrapeAshbyhqAsync, 'https://www.raincards.xyz',
                    'Web3 cards'),
        CompanyItem('exponential', 'https://jobs.ashbyhq.com/exponential', ScrapeAshbyhqAsync, 'https://exponential.fi',
                    'DeFi'),
        CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', ScrapeAshbyhqAsync, 'https://conduit.xyz',
                    'Infrastructure'),
        CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', ScrapeAshbyhqAsync, 'https://www.kiln.fi',
                    'Staking & Infra'),
        CompanyItem("flashbots", "https://jobs.ashbyhq.com/flashbots.net", ScrapeAshbyhqAsync,
                    "https://www.flashbots.net", "ETH MEV"),
        CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', ScrapeAshbyhqAsync, 'https://www.paradigm.xyz',
                    'Web3 financing'),
        CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhqAsync, 'https://dune.com',
                    'Web3 data'),
        CompanyItem("solanafoundation", "https://jobs.ashbyhq.com/Solana%20Foundation", ScrapeAshbyhqAsync,
                    "https://solana.org", "Blockchain"),
        CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhqAsync, 'https://syndica.io',
                    'Infrastructure'),
        CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhqAsync,
                    'https://ellipsislabs.xyz', 'Trading Protocol'),
        CompanyItem("kraken", "https://jobs.lever.co/kraken", ScrapeLeverAsync, "https://kraken.com", "Exchange"),
        CompanyItem('arbitrumfoundation', 'https://jobs.lever.co/arbitrumfoundation', ScrapeLeverAsync,
                    'https://arbitrum.foundation', 'Layer 2'),
        CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLeverAsync, "https://chain.link",
                    "Blockchain"),
        CompanyItem('ethglobal', 'https://jobs.lever.co/ETHGlobal', ScrapeLeverAsync, 'https://ethglobal.com',
                    'Community'),
        CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', ScrapeLeverAsync, 'https://multiversx.com',
                    'Blockchain'),
        CompanyItem('sprucesystems', 'https://jobs.lever.co/sprucesystems', ScrapeLeverAsync, 'https://spruceid.com',
                    'Web3 ID'),
        CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', ScrapeLeverAsync, 'https://www.blockswap.network',
                    'Infra'),
        CompanyItem('Metatheory', 'https://jobs.lever.co/Metatheory', ScrapeLeverAsync,
                    'https://www.duskbreakers.gg', 'Web3 game'),
        CompanyItem('axiomzen', 'https://jobs.lever.co/axiomzen', ScrapeLeverAsync, 'https://www.axiomzen.com', 'Web3'),
        CompanyItem('fuellabs', 'https://jobs.lever.co/fuellabs', ScrapeLeverAsync, 'https://www.fuel.network',
                    'Blockchain'),
        CompanyItem('harmony', 'https://jobs.lever.co/harmony', ScrapeLeverAsync, 'https://www.harmony.one',
                    'Blockchain'),
        CompanyItem('wintermute', 'https://jobs.lever.co/wintermute-trading', ScrapeLeverAsync,
                    'https://www.wintermute.com',
                    'Trading'),
        CompanyItem("kaiko", "https://jobs.eu.lever.co/kaiko", ScrapeLeverAsync, "https://www.kaiko.com", "Data"),
        CompanyItem('bebop', 'https://jobs.lever.co/Bebop', ScrapeLeverAsync, 'https://bebop.xyz', 'DeFi Exchange'),
        CompanyItem("Coinshift", "https://jobs.lever.co/Coinshift", ScrapeLeverAsync, "https://coinshift.xyz",
                    "Custody software"),
        CompanyItem("swissborg", "https://jobs.lever.co/swissborg", ScrapeLeverAsync, "https://swissborg.com",
                    "Exchange"),
        CompanyItem("OpenSea", "https://jobs.lever.co/OpenSea", ScrapeLeverAsync, "https://opensea.io", "NFT"),
        CompanyItem("storyprotocol", "https://jobs.lever.co/storyprotocol", ScrapeLeverAsync,
                    "https://www.storyprotocol.xyz", "Protocol"),
        CompanyItem("ethereumfoundation", "https://jobs.lever.co/ethereumfoundation", ScrapeLeverAsync,
                    "https://ethereum.org", "Blockchain"),
        CompanyItem("aave", "https://jobs.eu.lever.co/aave", ScrapeLeverAsync, "https://aave.com", "Protocol"),
        CompanyItem("crypto", "https://jobs.lever.co/crypto", ScrapeLeverAsync, "https://crypto.com", "Exchange"),
        CompanyItem("Luxor", "https://jobs.lever.co/LuxorTechnology", ScrapeLeverAsync, "https://www.luxor.tech",
                    "Mining"),
        CompanyItem("anchorage", "https://jobs.lever.co/anchorage", ScrapeLeverAsync, "https://www.anchorage.com",
                    "Trading"),
        CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLeverAsync, "https://www.biconomy.io",
                    "Infra"),
        CompanyItem('enso', 'https://jobs.lever.co/Enso', ScrapeLeverAsync, 'https://www.enso.finance', 'DeFi'),
        CompanyItem("Polygon", "https://jobs.lever.co/Polygon", ScrapeLeverAsync, "https://polygon.technology",
                    "Blockchain"),
        CompanyItem("tokenmetrics", "https://jobs.lever.co/tokenmetrics", ScrapeLeverAsync,
                    "https://www.tokenmetrics.com", "Information"),
        CompanyItem("offchainlabs", "https://jobs.lever.co/offchainlabs", ScrapeLeverAsync,
                    "https://offchainlabs.com", "Protocol"),
        CompanyItem("subspacelabs", "https://jobs.lever.co/subspacelabs", ScrapeLeverAsync,
                    "https://subspace.network", "Blockchain Infra"),
        CompanyItem('3boxlabs', 'https://jobs.lever.co/3box', ScrapeLeverAsync, 'https://3boxlabs.com',
                    'Infra'),
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
        CompanyItem("immutable", "https://jobs.lever.co/immutable", ScrapeLeverAsync, "https://www.immutable.com",
                    "NFT"),
        CompanyItem("web3auth", "https://jobs.lever.co/TorusLabs", ScrapeLeverAsync, "https://web3auth.io", "Auth"),
        CompanyItem("cere-network", "https://jobs.lever.co/cere-network", ScrapeLeverAsync, "https://cere.network",
                    "Infra"),
        CompanyItem('matterlabs', 'https://jobs.eu.lever.co/matterlabs', ScrapeLeverAsync, 'https://matter-labs.io',
                    'Protocol'),
        CompanyItem("hiro", "https://jobs.lever.co/hiro", ScrapeLeverAsync, "https://www.hiro.so", "Infra"),
        CompanyItem('AQX', 'https://jobs.lever.co/presto', ScrapeLeverAsync, 'https://aqx.com', 'Exchange and Web3'),
        CompanyItem('ultra', 'https://jobs.lever.co/ultra', ScrapeLeverAsync,
                    'https://ultra.io', 'Web3 Gaming'),
        CompanyItem('bitwise', 'https://jobs.lever.co/bitwiseinvestments', ScrapeLeverAsync,
                    'https://bitwiseinvestments.com', 'Asset Management'),
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
        # 66.46 sec for 56 company names
