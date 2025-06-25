from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever

company_list = [
    CompanyItem('ethenalabs', 'https://jobs.lever.co/ethenalabs', ScrapeLever,
                'https://www.ethena.fi'),
    CompanyItem('arbitrumfoundation', 'https://jobs.lever.co/arbitrumfoundation', ScrapeLever,
                'https://arbitrum.foundation'),
    CompanyItem('3boxlabs', 'https://jobs.lever.co/3box', ScrapeLever, 'https://3boxlabs.com'),
    CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', ScrapeLever, 'https://www.blockswap.network'),
    CompanyItem('wintermute', 'https://jobs.lever.co/wintermute-trading', ScrapeLever, 'https://www.wintermute.com'),
    CompanyItem('sprucesystems', 'https://jobs.lever.co/sprucesystems', ScrapeLever, 'https://spruceid.com'),
    CompanyItem('royal', 'https://jobs.lever.co/Royal', ScrapeLever, 'https://royal.io'),
    CompanyItem('enso', 'https://jobs.lever.co/Enso', ScrapeLever, 'https://www.enso.finance'),
    CompanyItem('gauntlet', 'https://jobs.lever.co/gauntlet', ScrapeLever, 'https://gauntlet.network'),
    CompanyItem('AQX', 'https://jobs.lever.co/presto', ScrapeLever, 'https://aqx.com'),
    CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', ScrapeLever, 'https://multiversx.com'),
    CompanyItem('matterlabs', 'https://jobs.eu.lever.co/matterlabs', ScrapeLever, 'https://matter-labs.io'),
    CompanyItem('fuellabs', 'https://jobs.lever.co/fuellabs', ScrapeLever, 'https://www.fuel.network'),
    CompanyItem("Luxor", "https://jobs.lever.co/LuxorTechnology", ScrapeLever, "https://www.luxor.tech"),
    CompanyItem("anchorage", "https://jobs.lever.co/anchorage", ScrapeLever, "https://www.anchorage.com"),
    CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLever, "https://www.biconomy.io"),
    CompanyItem("kraken", "https://jobs.lever.co/kraken", ScrapeLever, "https://kraken.com"),
    CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLever, "https://chain.link"),
    CompanyItem("hiro", "https://jobs.lever.co/hiro", ScrapeLever, "https://www.hiro.so"),
    CompanyItem("kaiko", "https://jobs.eu.lever.co/kaiko", ScrapeLever, "https://www.kaiko.com"),
    CompanyItem("tessera", "https://jobs.lever.co/ftc", ScrapeLever, "https://tessera.co"),
    CompanyItem("cere-network", "https://jobs.lever.co/cere-network", ScrapeLever, "https://cere.network"),
    CompanyItem("ramp.network", "https://jobs.lever.co/careers.ramp.network", ScrapeLever, "https://ramp.network"),
    CompanyItem("ledger", "https://jobs.lever.co/ledger", ScrapeLever, "https://www.ledger.com"),
    CompanyItem("request", "https://jobs.lever.co/request", ScrapeLever, "https://request.network"),
    CompanyItem("immutable", "https://jobs.lever.co/immutable", ScrapeLever, "https://www.immutable.com"),
    CompanyItem("web3auth", "https://jobs.lever.co/TorusLabs", ScrapeLever, "https://web3auth.io")]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

for company in company_list:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
