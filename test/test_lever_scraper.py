from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever

company_list = [
    CompanyItem('wintermute', 'https://jobs.lever.co/wintermute-trading', ScrapeLever, 'https://www.wintermute.com',
                'Trading'),
    CompanyItem('AQX', 'https://jobs.lever.co/AQX', ScrapeLever, 'https://aqx.com', 'Exchange and Web3'),
    CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', ScrapeLever, 'https://multiversx.com', 'Blockchain'),
    CompanyItem('matterlabs', 'https://jobs.eu.lever.co/matterlabs', ScrapeLever, 'https://matter-labs.io', 'Protocol'),
    CompanyItem('fuellabs', 'https://jobs.lever.co/fuellabs', ScrapeLever, 'https://www.fuel.network', 'Blockchain'),
    CompanyItem("Luxor", "https://jobs.lever.co/LuxorTechnology", ScrapeLever, "https://www.luxor.tech", "Mining"),
    CompanyItem("anchorage", "https://jobs.lever.co/anchorage", ScrapeLever, "https://www.anchorage.com", "Trading"),
    CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLever, "https://www.biconomy.io", "Infra"),
    CompanyItem("kraken", "https://jobs.lever.co/kraken", ScrapeLever, "https://kraken.com", "Exchange"),
    CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLever, "https://chain.link", "Blockchain"),
    CompanyItem("hiro", "https://jobs.lever.co/hiro", ScrapeLever, "https://www.hiro.so", "Infra"),
    CompanyItem("kaiko", "https://jobs.eu.lever.co/kaiko", ScrapeLever, "https://www.kaiko.com", "Data"),
    CompanyItem("tessera", "https://jobs.lever.co/ftc", ScrapeLever, "https://tessera.co", "NFT"),
    CompanyItem("cere-network", "https://jobs.lever.co/cere-network", ScrapeLever, "https://cere.network", "Infra"),
    CompanyItem("ramp.network", "https://jobs.lever.co/careers.ramp.network", ScrapeLever, "https://ramp.network",
                "Payments"),
    CompanyItem("ledger", "https://jobs.lever.co/ledger", ScrapeLever, "https://www.ledger.com", "Wallet"),
    CompanyItem("request", "https://jobs.lever.co/request", ScrapeLever, "https://request.network", "Payments"),
    CompanyItem("immutable", "https://jobs.lever.co/immutable", ScrapeLever, "https://www.immutable.com", "NFT"),
    CompanyItem("web3auth", "https://jobs.lever.co/TorusLabs", ScrapeLever, "https://web3auth.io", "Auth")]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

for company in company_list:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
