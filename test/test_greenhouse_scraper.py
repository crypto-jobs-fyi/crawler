from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_greenhouse import ScrapeGreenhouse

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('grayscaleinvestments', 'https://boards.greenhouse.io/grayscaleinvestments', ScrapeGreenhouse,
                'https://grayscale.com'),
    CompanyItem('dragonflycapital', 'https://boards.greenhouse.io/dragonflycapital', ScrapeGreenhouse,
                'https://www.dragonfly.xyz'),
    CompanyItem('penumbralabs', 'https://boards.greenhouse.io/penumbralabs', ScrapeGreenhouse,
                'https://eco.com'),
    CompanyItem('econetwork', 'https://boards.greenhouse.io/econetwork', ScrapeGreenhouse,
                'https://eco.com'),
    CompanyItem('outlierventures', 'https://boards.eu.greenhouse.io/outlierventures', ScrapeGreenhouse,
                'https://outlierventures.io'),
    CompanyItem('evmos', 'https://boards.eu.greenhouse.io/evmos', ScrapeGreenhouse, 'https://evmos.org'),
    CompanyItem('magic', 'https://boards.greenhouse.io/magic', ScrapeGreenhouse, 'https://magic.link'),
    CompanyItem('trmlabs', 'https://www.trmlabs.com/careers-list', ScrapeGreenhouse,
                'https://www.trmlabs.com'),
    CompanyItem('foundrydigital', 'https://boards.greenhouse.io/foundrydigital', ScrapeGreenhouse,
                'https://foundrydigital.com'),
    CompanyItem('o1labs', 'https://boards.greenhouse.io/o1labs', ScrapeGreenhouse, 'https://o1labs.org'),
    CompanyItem('orderlynetwork', 'https://boards.greenhouse.io/orderlynetwork', ScrapeGreenhouse,
                'https://orderly.network'),
    CompanyItem('paradigm.co', 'https://boards.greenhouse.io/paradigm62', ScrapeGreenhouse, 'https://www.paradigm.co'),
    CompanyItem('immunefi', 'https://boards.greenhouse.io/immunefi', ScrapeGreenhouse, 'https://immunefi.com'),
    CompanyItem('protocollabs', 'https://boards.greenhouse.io/protocollabs', ScrapeGreenhouse,
                'https://protocol.ai/about'),
    CompanyItem('taxbit', 'https://boards.greenhouse.io/taxbit', ScrapeGreenhouse, 'https://taxbit.com'),
    CompanyItem('osmosisdex', 'https://boards.greenhouse.io/osmosisdex', ScrapeGreenhouse, 'https://osmosis.zone'),
    CompanyItem('stellar', 'https://boards.greenhouse.io/stellar', ScrapeGreenhouse, 'https://stellar.org'),
    CompanyItem('bitfury', 'https://boards.greenhouse.io/bitfury', ScrapeGreenhouse, 'https://bitfury.com'),
    CompanyItem('mobilecoin', 'https://boards.greenhouse.io/mobilecoin', ScrapeGreenhouse,
                'https://mobilecoin.com'),
    CompanyItem('chia', 'https://www.chia.net/careers', ScrapeGreenhouse,
                'https://www.chia.net'),
    CompanyItem("solanafoundation", "https://boards.greenhouse.io/solanafoundation", ScrapeGreenhouse,
                "https://solana.org"),
    CompanyItem("worldcoinorg", "https://boards.greenhouse.io/worldcoinorg", ScrapeGreenhouse,
                "https://worldcoin.org"),
    CompanyItem("edgeandnode", "https://boards.greenhouse.io/edgeandnode", ScrapeGreenhouse,
                "https://edgeandnode.com"),
    CompanyItem("clearmatics", "https://boards.greenhouse.io/clearmatics", ScrapeGreenhouse,
                "https://www.clearmatics.com"),
    CompanyItem("aztec", "https://boards.eu.greenhouse.io/aztec", ScrapeGreenhouse, "https://aztec.network"),
    CompanyItem("avalabs", "https://boards.greenhouse.io/avalabs", ScrapeGreenhouse,
                "https://www.avalabs.org"),
    CompanyItem("galaxydigitalservices", "https://boards.greenhouse.io/galaxydigitalservices",
                ScrapeGreenhouse, "https://www.galaxy.com"),
    CompanyItem("bittrex", "https://boards.greenhouse.io/bittrex", ScrapeGreenhouse,
                "https://global.bittrex.com"),
    CompanyItem("EigenLabs", "https://boards.greenhouse.io/layrlabs", ScrapeGreenhouse,
                "https://www.v1.eigenlayer.xyz"),
    CompanyItem("kadena", "https://boards.greenhouse.io/kadenallc", ScrapeGreenhouse, "https://kadena.io"),
    CompanyItem("poap", "https://boards.greenhouse.io/poaptheproofofattendanceprotocol", ScrapeGreenhouse,
                "https://poap.xyz"),
    CompanyItem("chainsafesystems", "https://boards.greenhouse.io/chainsafesystems", ScrapeGreenhouse,
                "https://chainsafe.io"),
    CompanyItem("status", "https://jobs.status.im", ScrapeGreenhouse, "https://status.im"),
    CompanyItem("digitalasset", "https://boards.greenhouse.io/digitalasset", ScrapeGreenhouse,
                "https://www.digitalasset.com"),
    CompanyItem("copperco", "https://boards.eu.greenhouse.io/copperco", ScrapeGreenhouse,
                "https://copper.co"),
    CompanyItem("messari", "https://boards.greenhouse.io/messari", ScrapeGreenhouse, "https://messari.io"),
    CompanyItem("layerzerolabs", "https://boards.greenhouse.io/layerzerolabs", ScrapeGreenhouse,
                "https://layerzero.network"),
    CompanyItem("jumpcrypto", "https://boards.greenhouse.io/jumpcrypto", ScrapeGreenhouse,
                "https://jumpcrypto.com"),
    CompanyItem("oasisnetwork", "https://boards.greenhouse.io/oasisnetwork", ScrapeGreenhouse,
                "https://oasisprotocol.org")]

for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()
