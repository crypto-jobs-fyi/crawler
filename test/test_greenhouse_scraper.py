from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_greenhouse import ScrapeGreenhouse

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [CompanyItem('stellar', 'https://boards.greenhouse.io/stellar', ScrapeGreenhouse, 'https://stellar.org',
                            'Blockchain'),
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
                CompanyItem("paxos", "https://paxos.com/careers/role", ScrapeGreenhouse, "https://paxos.com",
                            "Stable Coin"),
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
    print(company.jobs_url)
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()
