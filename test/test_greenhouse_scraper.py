from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_greenhouse import ScrapeGreenhouse

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('econetwork', 'https://boards.greenhouse.io/econetwork', ScrapeGreenhouse,
                'https://eco.com', 'Web3 wallet'),
    CompanyItem('outlierventures', 'https://boards.eu.greenhouse.io/outlierventures', ScrapeGreenhouse,
                'https://outlierventures.io', 'Web3 Ventures'),
    CompanyItem('evmos', 'https://boards.eu.greenhouse.io/evmos', ScrapeGreenhouse, 'https://evmos.org',
                'Cross-Chain Connectivity'),
    CompanyItem('magic', 'https://boards.greenhouse.io/magic', ScrapeGreenhouse, 'https://magic.link', 'Web3 Wallets'),
    CompanyItem('trmlabs', 'https://www.trmlabs.com/careers-list', ScrapeGreenhouse,
                'https://www.trmlabs.com', 'Web3 Information'),
    CompanyItem('foundrydigital', 'https://boards.greenhouse.io/foundrydigital', ScrapeGreenhouse,
                'https://foundrydigital.com', 'Web3'),
    CompanyItem('o1labs', 'https://boards.greenhouse.io/o1labs', ScrapeGreenhouse, 'https://o1labs.org',
                'Web3'),
    CompanyItem('orderlynetwork', 'https://boards.greenhouse.io/orderlynetwork', ScrapeGreenhouse,
                'https://orderly.network', 'Exchange'),
    CompanyItem('paradigm.co', 'https://boards.greenhouse.io/paradigm62', ScrapeGreenhouse, 'https://www.paradigm.co',
                'Liquidity'),
    CompanyItem('immunefi', 'https://boards.greenhouse.io/immunefi', ScrapeGreenhouse, 'https://immunefi.com',
                'Bug bounty platform'),
    CompanyItem('protocollabs', 'https://boards.greenhouse.io/protocollabs', ScrapeGreenhouse, 'https://protocol.ai/about',
                'Web3 IPFS research platform'),
    CompanyItem('taxbit', 'https://boards.greenhouse.io/taxbit', ScrapeGreenhouse, 'https://taxbit.com', 'Accounting'),
    CompanyItem('osmosisdex', 'https://boards.greenhouse.io/osmosisdex', ScrapeGreenhouse, 'https://osmosis.zone',
                'Exchange'),
    CompanyItem('stellar', 'https://boards.greenhouse.io/stellar', ScrapeGreenhouse, 'https://stellar.org',
                'Blockchain'),
    CompanyItem('bitfury', 'https://boards.greenhouse.io/bitfury', ScrapeGreenhouse, 'https://bitfury.com',
                'Web3'),
    CompanyItem('mobilecoin', 'https://boards.greenhouse.io/mobilecoin', ScrapeGreenhouse,
                'https://mobilecoin.com', 'Blockchain'),
    CompanyItem('chia', 'https://www.chia.net/careers', ScrapeGreenhouse,
                'https://www.chia.net', 'Blockchain'),
    CompanyItem('okcoin', 'https://boards.greenhouse.io/okcoin', ScrapeGreenhouse, 'https://www.okcoin.com',
                'Exchange'),
    CompanyItem("solanafoundation", "https://boards.greenhouse.io/solanafoundation", ScrapeGreenhouse,
                "https://solana.org", "Blockchain"),
    CompanyItem("worldcoinorg", "https://boards.greenhouse.io/worldcoinorg", ScrapeGreenhouse,
                "https://worldcoin.org", "Blockchain"),
    CompanyItem("edgeandnode", "https://boards.greenhouse.io/edgeandnode", ScrapeGreenhouse,
                "https://edgeandnode.com", "Infra"),
    CompanyItem("clearmatics", "https://boards.greenhouse.io/clearmatics", ScrapeGreenhouse,
                "https://www.clearmatics.com", "Protocol"),
    CompanyItem("aztec", "https://boards.eu.greenhouse.io/aztec", ScrapeGreenhouse, "https://aztec.network",
                "Protocol"),
    CompanyItem("avalabs", "https://boards.greenhouse.io/avalabs", ScrapeGreenhouse,
                "https://www.avalabs.org", "Blockchain"),
    CompanyItem("galaxydigitalservices", "https://boards.greenhouse.io/galaxydigitalservices",
                ScrapeGreenhouse, "https://www.galaxy.com", 'Trading'),
    CompanyItem("bittrex", "https://boards.greenhouse.io/bittrex", ScrapeGreenhouse,
                "https://global.bittrex.com", 'Exchange'),
    CompanyItem("bitcoin", "https://www.bitcoin.com/jobs/#joblist", ScrapeGreenhouse,
                "https://www.bitcoin.com", 'Exchange'),
    CompanyItem("EigenLabs", "https://boards.greenhouse.io/layrlabs", ScrapeGreenhouse,
                "https://www.v1.eigenlayer.xyz", "Infra"),
    CompanyItem("kadena", "https://boards.greenhouse.io/kadenallc", ScrapeGreenhouse, "https://kadena.io",
                "PoW chain"),
    CompanyItem("poap", "https://boards.greenhouse.io/poaptheproofofattendanceprotocol", ScrapeGreenhouse,
                "https://poap.xyz", "Protocol"),
    CompanyItem("chainsafesystems", "https://boards.greenhouse.io/chainsafesystems", ScrapeGreenhouse,
                "https://chainsafe.io", "Infra"),
    CompanyItem("status", "https://jobs.status.im", ScrapeGreenhouse, "https://status.im", "Messanger"),
    CompanyItem("digitalasset", "https://boards.greenhouse.io/digitalasset", ScrapeGreenhouse,
                "https://www.digitalasset.com", "Custody"),
    CompanyItem("copperco", "https://boards.eu.greenhouse.io/copperco", ScrapeGreenhouse,
                "https://copper.co", "Custody"),
    CompanyItem("messari", "https://boards.greenhouse.io/messari", ScrapeGreenhouse, "https://messari.io",
                "Information"),
    CompanyItem("layerzerolabs", "https://boards.greenhouse.io/layerzerolabs", ScrapeGreenhouse,
                "https://layerzero.network", "Infra"),
    CompanyItem("jumpcrypto", "https://boards.greenhouse.io/jumpcrypto", ScrapeGreenhouse,
                "https://jumpcrypto.com", "Infra"),
    CompanyItem("oasisnetwork", "https://boards.greenhouse.io/oasisnetwork", ScrapeGreenhouse,
                "https://oasisprotocol.org", "Protocol")]

for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()
