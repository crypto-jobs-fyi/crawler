import json

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_smartrecruiters import ScrapeSmartrecruiters
from src.scrape_recruitee import ScrapeRecruitee
from src.scrape_binance import ScrapeBinance
from src.scrape_bamboohr import ScrapeBamboohr
from src.scrape_consensys import ScrapeConsensys
from src.scrape_ripple import ScrapeRipple
from src.scrape_workable import ScrapeWorkable
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_paxos import ScrapePaxos


def get_company_list() -> []:
    return [CompanyItem("binance", "https://www.binance.com/en/careers/job-openings", ScrapeBinance,
                        "https://www.binance.com", "Exchange"),
            CompanyItem("kraken", "https://jobs.lever.co/kraken", ScrapeLever, "https://kraken.com", "Exchange"),
            CompanyItem('arbitrumfoundation', 'https://jobs.lever.co/arbitrumfoundation', ScrapeLever,
                        'https://arbitrum.foundation', 'Layer 2'),
            CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLever, "https://chain.link",
                        "Blockchain"),
            CompanyItem('ethglobal', 'https://jobs.lever.co/ETHGlobal', ScrapeLever, 'https://ethglobal.com',
                        'Community'),
            CompanyItem('blox-route', 'https://jobs.lever.co/blox-route', ScrapeLever,
                        'https://bloxroute.com', 'Web3 MEV DeFi infra'),
            CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', ScrapeLever, 'https://multiversx.com',
                        'Blockchain'),
            CompanyItem('sprucesystems', 'https://jobs.lever.co/sprucesystems', ScrapeLever, 'https://spruceid.com',
                        'Web3 ID'),
            CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', ScrapeLever, 'https://www.blockswap.network',
                        'Infra'),
            CompanyItem('Metatheory', 'https://jobs.lever.co/Metatheory', ScrapeLever,
                        'https://www.duskbreakers.gg', 'Web3 game'),
            CompanyItem('axiomzen', 'https://jobs.lever.co/axiomzen', ScrapeLever, 'https://www.axiomzen.com', 'Web3'),
            CompanyItem('fuellabs', 'https://jobs.lever.co/fuellabs', ScrapeLever, 'https://www.fuel.network',
                        'Blockchain'),
            CompanyItem('Notabene', 'https://jobs.lever.co/Notabene', ScrapeLever,
                        'https://notabene.id', 'Web3 Compliance'),
            CompanyItem('harmony', 'https://jobs.lever.co/harmony', ScrapeLever, 'https://www.harmony.one',
                        'Blockchain'),
            CompanyItem('wintermute', 'https://jobs.lever.co/wintermute-trading', ScrapeLever,
                        'https://www.wintermute.com',
                        'Trading'),
            CompanyItem('coinspaid', 'https://jobs.eu.lever.co/coinspaid', ScrapeLever,
                        'https://coinspaid.com', 'Web3 Payments'),
            CompanyItem("kaiko", "https://jobs.eu.lever.co/kaiko", ScrapeLever, "https://www.kaiko.com", "Data"),
            CompanyItem('bebop', 'https://jobs.lever.co/Bebop', ScrapeLever, 'https://bebop.xyz', 'DeFi Exchange'),
            CompanyItem("Coinshift", "https://jobs.lever.co/Coinshift", ScrapeLever, "https://coinshift.xyz",
                        "Custody software"),
            CompanyItem("swissborg", "https://jobs.lever.co/swissborg", ScrapeLever, "https://swissborg.com",
                        "Exchange"),
            CompanyItem("OpenSea", "https://jobs.lever.co/OpenSea", ScrapeLever, "https://opensea.io", "NFT"),
            CompanyItem("storyprotocol", "https://jobs.lever.co/storyprotocol", ScrapeLever,
                        "https://www.storyprotocol.xyz", "Protocol"),
            CompanyItem("ethereumfoundation", "https://jobs.lever.co/ethereumfoundation", ScrapeLever,
                        "https://ethereum.org", "Blockchain"),
            CompanyItem("aave", "https://jobs.eu.lever.co/aave", ScrapeLever, "https://aave.com", "Protocol"),
            CompanyItem("crypto", "https://jobs.lever.co/crypto", ScrapeLever, "https://crypto.com", "Exchange"),
            CompanyItem("Luxor", "https://jobs.lever.co/LuxorTechnology", ScrapeLever, "https://www.luxor.tech",
                        "Mining"),
            CompanyItem("anchorage", "https://jobs.lever.co/anchorage", ScrapeLever, "https://www.anchorage.com",
                        "Trading"),
            CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLever, "https://www.biconomy.io",
                        "Infra"),
            CompanyItem('enso', 'https://jobs.lever.co/Enso', ScrapeLever, 'https://www.enso.finance', 'DeFi'),
            CompanyItem("Polygon", "https://jobs.lever.co/Polygon", ScrapeLever, "https://polygon.technology",
                        "Blockchain"),
            CompanyItem("tokenmetrics", "https://jobs.lever.co/tokenmetrics", ScrapeLever,
                        "https://www.tokenmetrics.com", "Information"),
            CompanyItem("offchainlabs", "https://jobs.lever.co/offchainlabs", ScrapeLever,
                        "https://offchainlabs.com", "Protocol"),
            CompanyItem("subspacelabs", "https://jobs.lever.co/subspacelabs", ScrapeLever,
                        "https://subspace.network", "Blockchain Infra"),
            CompanyItem('3boxlabs', 'https://jobs.lever.co/3box', ScrapeLever, 'https://3boxlabs.com',
                        'Infra'),
            CompanyItem("ramp.network", "https://jobs.lever.co/careers.ramp.network", ScrapeLever,
                        "https://ramp.network", "Payments"),
            CompanyItem('risklabs', 'https://jobs.lever.co/risklabs', ScrapeLever, 'https://risklabs.foundation',
                        'Protocol'),
            CompanyItem('celestia', 'https://jobs.lever.co/celestia', ScrapeLever, 'https://celestia.org',
                        'Modular Blockchain'),
            CompanyItem('polymerlabs', 'https://jobs.lever.co/polymerlabs', ScrapeLever, 'https://www.polymerlabs.org',
                        'Modular Blockchain'),
            CompanyItem('royal', 'https://jobs.lever.co/Royal', ScrapeLever, 'https://royal.io', 'Web3 + Music'),
            CompanyItem('gauntlet', 'https://jobs.lever.co/gauntlet', ScrapeLever, 'https://gauntlet.network',
                        'Web3 + Financial Modelling'),
            CompanyItem("ledger", "https://jobs.lever.co/ledger", ScrapeLever, "https://www.ledger.com", "Wallet"),
            CompanyItem("request", "https://jobs.lever.co/request", ScrapeLever, "https://request.network",
                        "Payments"),
            CompanyItem("immutable", "https://jobs.lever.co/immutable", ScrapeLever, "https://www.immutable.com",
                        "NFT"),
            CompanyItem("web3auth", "https://jobs.lever.co/TorusLabs", ScrapeLever, "https://web3auth.io", "Auth"),
            CompanyItem("cere-network", "https://jobs.lever.co/cere-network", ScrapeLever, "https://cere.network",
                        "Infra"),
            CompanyItem('matterlabs', 'https://jobs.eu.lever.co/matterlabs', ScrapeLever, 'https://matter-labs.io',
                        'Protocol'),
            CompanyItem("hiro", "https://jobs.lever.co/hiro", ScrapeLever, "https://www.hiro.so", "Infra"),
            CompanyItem('AQX', 'https://jobs.lever.co/presto', ScrapeLever, 'https://aqx.com', 'Exchange and Web3'),
            CompanyItem('ultra', 'https://jobs.lever.co/ultra', ScrapeLever,
                        'https://ultra.io', 'Web3 Gaming'),
            CompanyItem('ethenalabs', 'https://jobs.lever.co/ethenalabs', ScrapeLever,
                        'https://www.ethena.fi', 'Web3 bonds'),
            CompanyItem('bitwise', 'https://jobs.lever.co/bitwiseinvestments', ScrapeLever,
                        'https://bitwiseinvestments.com', 'Asset Management'),
            CompanyItem('grayscaleinvestments', 'https://boards.greenhouse.io/grayscaleinvestments', ScrapeGreenhouse,
                        'https://grayscale.com', 'Web3 Asset Manager'),
            CompanyItem("0x", "https://boards.greenhouse.io/0x", ScrapeGreenhouse, "https://0x.org",
                        "Blockchain"),
            CompanyItem('econetwork', 'https://boards.greenhouse.io/econetwork', ScrapeGreenhouse,
                        'https://eco.com', 'Web3 wallet'),
            CompanyItem("bitcoin", "https://www.bitcoin.com/jobs/#joblist", ScrapeGreenhouse,
                        "https://www.bitcoin.com", 'Exchange'),
            CompanyItem('magic', 'https://boards.greenhouse.io/magic', ScrapeGreenhouse, 'https://magic.link',
                        'Web3 Wallets'),
            CompanyItem("chainstack", "https://chainstack.bamboohr.com/careers", ScrapeBamboohr,
                        "https://chainstack.com", "Infra"),
            CompanyItem("coinmarketcap", "https://careers.smartrecruiters.com/B6/coinmarketcap",
                        ScrapeSmartrecruiters, "https://coinmarketcap.com", "Information"),
            CompanyItem('evmos', 'https://boards.eu.greenhouse.io/evmos', ScrapeGreenhouse, 'https://evmos.org',
                        'Cross-Chain Connectivity'),
            CompanyItem('orderlynetwork', 'https://boards.greenhouse.io/orderlynetwork', ScrapeGreenhouse,
                        'https://orderly.network', 'Exchange'),
            CompanyItem('shardeum', 'https://boards.greenhouse.io/shardeumfoundation', ScrapeGreenhouse,
                        'https://shardeum.org', 'Web3 L1'),
            CompanyItem("paxos",
                        "https://paxos.com/job-posts/?_sft_department=engineering-data,finance-accounting,hr-talent,information-technology,legal,operations,product-management,risk-compliance&_sft_office=us",
                        ScrapePaxos, "https://paxos.com", "Stable Coin"),
            CompanyItem('dydxopsdao', 'https://apply.workable.com/dydx-operations-trust', ScrapeWorkable,
                        'https://dydxopsdao.com', 'Web3 DAO'),
            CompanyItem("zora", "https://boards.greenhouse.io/zora", ScrapeGreenhouse, "https://zora.co", "NFT"),
            CompanyItem('bitfury', 'https://boards.greenhouse.io/bitfury', ScrapeGreenhouse, 'https://bitfury.com',
                        'Web3'),
            CompanyItem("cexio", "https://cexio.bamboohr.com/jobs", ScrapeBamboohr, "https://cex.io", "Exchange"),
            CompanyItem("circle", "https://boards.greenhouse.io/circle", ScrapeGreenhouse, "https://circle.com",
                        "Stable Coin"),
            CompanyItem("status", "https://jobs.status.im", ScrapeGreenhouse, "https://status.im", "Messanger"),
            CompanyItem("OKX", "https://boards.greenhouse.io/OKX", ScrapeGreenhouse, "https://okx.com",
                        "Exchange"),
            CompanyItem("bittrex", "https://boards.greenhouse.io/bittrex", ScrapeGreenhouse,
                        "https://global.bittrex.com", 'Exchange'),
            CompanyItem("bitmex", "https://boards.greenhouse.io/bitmex", ScrapeGreenhouse, "https://bitmex.com",
                        "Exchange"),
            CompanyItem("bitgo", "https://boards.greenhouse.io/bitgo", ScrapeGreenhouse, "https://bitgo.com",
                        "Exchange"),
            CompanyItem("bitpanda", "https://boards.eu.greenhouse.io/bitpanda", ScrapeGreenhouse,
                        "https://bitpanda.com", "Exchange"),
            CompanyItem("uniswaplabs", "https://boards.greenhouse.io/uniswaplabs", ScrapeGreenhouse,
                        "https://uniswap.org", "Exchange Protocol"),
            CompanyItem('osmosisdex', 'https://boards.greenhouse.io/osmosisdex', ScrapeGreenhouse,
                        'https://osmosis.zone',
                        'Exchange'),
            CompanyItem("moonpay", "https://boards.greenhouse.io/moonpay", ScrapeGreenhouse,
                        "https://www.moonpay.com", "Payments"),
            CompanyItem('penumbralabs', 'https://boards.greenhouse.io/penumbralabs', ScrapeGreenhouse,
                        'https://eco.com', 'Web3 trading'),
            CompanyItem("blockdaemon", "https://boards.greenhouse.io/blockdaemon", ScrapeGreenhouse,
                        "https://www.blockdaemon.com", "Staking & Infra"),
            CompanyItem("figment", "https://boards.greenhouse.io/figment", ScrapeGreenhouse,
                        "https://www.figment.io", "Staking & Infra"),
            CompanyItem('center', 'https://jobs.ashbyhq.com/center', ScrapeAshbyhq,
                        'https://center.app', 'Web3 NFT Data'),
            CompanyItem('Sui.Foundation', 'https://jobs.ashbyhq.com/Sui%20Foundation', ScrapeAshbyhq,
                        'https://sui.io', 'Web3 blockchain'),
            CompanyItem('rain', 'https://jobs.ashbyhq.com/rain', ScrapeAshbyhq, 'https://www.raincards.xyz',
                        'Web3 cards'),
            CompanyItem('exponential', 'https://jobs.ashbyhq.com/exponential', ScrapeAshbyhq, 'https://exponential.fi',
                        'DeFi'),
            CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', ScrapeAshbyhq, 'https://conduit.xyz',
                        'Infrastructure'),
            CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', ScrapeAshbyhq, 'https://www.kiln.fi',
                        'Staking & Infra'),
            CompanyItem("flashbots", "https://jobs.ashbyhq.com/flashbots.net", ScrapeAshbyhq,
                        "https://www.flashbots.net", "ETH MEV"),
            CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', ScrapeAshbyhq, 'https://www.paradigm.xyz',
                        'Web3 financing'),
            CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhq, 'https://dune.com',
                        'Web3 data'),
            CompanyItem("solanafoundation", "https://jobs.ashbyhq.com/Solana%20Foundation", ScrapeAshbyhq,
                        "https://solana.org", "Blockchain"),
            CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhq, 'https://syndica.io',
                        'Infrastructure'),
            CompanyItem('Blockworks', 'https://jobs.ashbyhq.com/Blockworks', ScrapeAshbyhq,
                        'https://blockworks.co', 'Web3 News'),
            CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhq,
                        'https://ellipsislabs.xyz', 'Trading Protocol'),
            CompanyItem('safe.global', 'https://jobs.ashbyhq.com/safe.global', ScrapeAshbyhq,
                        'https://safe.global', 'Web3 custody'),
            CompanyItem('RabbitHole', 'https://jobs.ashbyhq.com/RabbitHole', ScrapeAshbyhq,
                        'https://rabbithole.gg', 'Web3 gaming'),
            CompanyItem('Keyrock', 'https://jobs.ashbyhq.com/Keyrock', ScrapeAshbyhq,
                        'https://keyrock.eu', 'Web3 market maker'),
            CompanyItem('sound.xyz', 'https://jobs.ashbyhq.com/sound.xyz', ScrapeAshbyhq,
                        'https://www.sound.xyz', 'Web3 audio'),
            CompanyItem("quiknodeinc", "https://boards.greenhouse.io/quiknodeinc", ScrapeGreenhouse,
                        "https://www.quicknode.com", "Staking & Infra"),
            CompanyItem('21co', 'https://boards.greenhouse.io/21co', ScrapeGreenhouse,
                        'https://www.21.co', 'Web3 DeFi ETP'),
            CompanyItem('xapo', 'https://boards.greenhouse.io/xapo61', ScrapeGreenhouse,
                        'https://www.xapobank.com', 'Web3 bank'),
            CompanyItem('dragonflycapital', 'https://boards.greenhouse.io/dragonflycapital', ScrapeGreenhouse,
                        'https://www.dragonfly.xyz', 'Web3 funding'),
            CompanyItem("exodus54", "https://boards.greenhouse.io/exodus54", ScrapeGreenhouse,
                        "https://www.exodus.com", "Wallet"),
            CompanyItem("alchemy", "https://boards.greenhouse.io/alchemy", ScrapeGreenhouse,
                        "https://www.alchemy.com", "Dev & Infra"),
            CompanyItem("chainalysis", "https://boards.greenhouse.io/chainalysis", ScrapeGreenhouse,
                        "https://www.chainalysis.com", "Crypto Research"),
            CompanyItem("magiceden", "https://boards.greenhouse.io/magiceden", ScrapeGreenhouse,
                        "https://www.magiceden.io", "NFT"),
            CompanyItem("aztec", "https://boards.eu.greenhouse.io/aztec", ScrapeGreenhouse,
                        "https://aztec.network", "Protocol"),
            CompanyItem("nethermind", "https://boards.eu.greenhouse.io/nethermind", ScrapeGreenhouse,
                        "https://nethermind.io", "Crypto software"),
            CompanyItem("dfinity", "https://boards.greenhouse.io/dfinity", ScrapeGreenhouse, "https://dfinity.org",
                        "Blockchain"),
            CompanyItem('stellar', 'https://boards.greenhouse.io/stellar', ScrapeGreenhouse,
                        'https://stellar.org', 'Blockchain'),
            CompanyItem("parity", "https://boards.greenhouse.io/parity", ScrapeGreenhouse, "https://www.parity.io",
                        "Infra"),
            CompanyItem("optimism", "https://boards.greenhouse.io/optimism", ScrapeGreenhouse,
                        "https://www.optimism.io", "L2 protocol"),
            CompanyItem('coinmetrics', 'https://boards.greenhouse.io/coinmetrics', ScrapeGreenhouse,
                        'https://coinmetrics.io', 'Web3 Data'),
            CompanyItem("oplabs", "https://boards.greenhouse.io/oplabs", ScrapeGreenhouse, "https://www.oplabs.co",
                        "L2 protocol"),
            CompanyItem('goldsky', 'https://boards.greenhouse.io/goldsky', ScrapeGreenhouse,
                        'https://goldsky.com', 'Web3 Data'),
            CompanyItem('outlierventures', 'https://boards.eu.greenhouse.io/outlierventures', ScrapeGreenhouse,
                        'https://outlierventures.io', 'Web3 Ventures'),
            CompanyItem('walletconnect', 'https://apply.workable.com/walletconnect', ScrapeWorkable,
                        'https://walletconnect.com', 'Web3 Wallet Infra'),
            CompanyItem('prepo', 'https://apply.workable.com/prepo', ScrapeWorkable,
                        'https://prepo.io', 'Web3 pre-IPO trading'),
            CompanyItem('clockwork-labs', 'https://apply.workable.com/clockwork-labs',
                        ScrapeWorkable, 'https://clockworklabs.io', 'Web3 gaming'),
            CompanyItem("bitfinex", "https://bitfinex.recruitee.com", ScrapeRecruitee, "https://www.bitfinex.com",
                        "Exchange"),
            CompanyItem('o1labs', 'https://boards.greenhouse.io/o1labs', ScrapeGreenhouse, 'https://o1labs.org',
                        'Web3'),
            CompanyItem('paradigm.co', 'https://boards.greenhouse.io/paradigm62', ScrapeGreenhouse,
                        'https://www.paradigm.co',
                        'Liquidity'),
            CompanyItem("trustwallet", "https://careers.smartrecruiters.com/B6/trustwallet", ScrapeSmartrecruiters,
                        "https://trustwallet.com", "Wallet"),
            CompanyItem("Swissquote", "https://careers.smartrecruiters.com/Swissquote", ScrapeSmartrecruiters,
                        "https://en.swissquote.com", "Exchange"),
            CompanyItem('taxbit', 'https://boards.greenhouse.io/taxbit', ScrapeGreenhouse, 'https://taxbit.com',
                        'Accounting'),
            CompanyItem("avalabs", "https://boards.greenhouse.io/avalabs", ScrapeGreenhouse,
                        "https://www.avalabs.org", "Blockchain"),
            CompanyItem("aptoslabs", "https://boards.greenhouse.io/aptoslabs", ScrapeGreenhouse,
                        "https://aptoslabs.com",
                        "Blockchain"),
            CompanyItem("filecoinfoundation", "https://boards.greenhouse.io/filecoinfoundation", ScrapeGreenhouse,
                        "https://fil.org", "Blockchain"),
            CompanyItem('foundrydigital', 'https://boards.greenhouse.io/foundrydigital', ScrapeGreenhouse,
                        'https://foundrydigital.com', 'Web3 Infra'),
            CompanyItem('immunefi', 'https://boards.greenhouse.io/immunefi', ScrapeGreenhouse, 'https://immunefi.com',
                        'Bug bounty platform'),
            CompanyItem('wirex', 'https://wirex.bamboohr.com/careers', ScrapeBamboohr, 'https://wirexapp.com',
                        'Web3 card'),
            CompanyItem('protocollabs', 'https://boards.greenhouse.io/protocollabs', ScrapeGreenhouse,
                        'https://protocol.ai/about',
                        'Web3 IPFS research platform'),
            CompanyItem('trmlabs', 'https://www.trmlabs.com/careers-list', ScrapeGreenhouse,
                        'https://www.trmlabs.com', 'Web3 Information'),
            CompanyItem("messari", "https://boards.greenhouse.io/messari", ScrapeGreenhouse, "https://messari.io",
                        "Web3 Information"),
            CompanyItem("serotonin", "https://boards.greenhouse.io/serotonin", ScrapeGreenhouse, "https://serotonin.co",
                        "Information"),
            CompanyItem("copperco", "https://boards.eu.greenhouse.io/copperco", ScrapeGreenhouse,
                        "https://copper.co", "Custody"),
            CompanyItem("digitalasset", "https://boards.greenhouse.io/digitalasset", ScrapeGreenhouse,
                        "https://www.digitalasset.com", "Custody"),
            CompanyItem("layerzerolabs", "https://boards.greenhouse.io/layerzerolabs", ScrapeGreenhouse,
                        "https://layerzero.network", "Infra"),
            CompanyItem('okcoin', 'https://boards.greenhouse.io/okcoin', ScrapeGreenhouse,
                        'https://www.okcoin.com', 'Exchange'),
            CompanyItem("oasisnetwork", "https://boards.greenhouse.io/oasisnetwork", ScrapeGreenhouse,
                        "https://oasisprotocol.org", "Protocol"),
            CompanyItem("consensys", "https://consensys.net/open-roles", ScrapeConsensys, "https://consensys.net",
                        "Infra"),
            CompanyItem("ankr", "https://boards.greenhouse.io/ankrnetwork", ScrapeGreenhouse,
                        "https://www.ankr.com", "Web3 Staking Protocol"),
            CompanyItem("chainsafesystems", "https://boards.greenhouse.io/chainsafesystems", ScrapeGreenhouse,
                        "https://chainsafe.io", "Infra"),
            CompanyItem("ripple", "https://ripple.com/careers/all-jobs", ScrapeRipple, "https://ripple.com",
                        "Blockchain"),
            CompanyItem("kadena", "https://boards.greenhouse.io/kadenallc", ScrapeGreenhouse, "https://kadena.io",
                        "Blockchain"),
            CompanyItem("eigenlabs", "https://boards.greenhouse.io/eigenlabs", ScrapeGreenhouse,
                        "https://www.eigenlayer.xyz", "Infra"),
            CompanyItem('sygnum', 'https://sygnum.bamboohr.com/careers', ScrapeBamboohr, 'https://www.sygnum.com',
                        'Crypto bank'),
            CompanyItem("galaxydigitalservices", "https://boards.greenhouse.io/galaxydigitalservices",
                        ScrapeGreenhouse, "https://www.galaxy.com", 'Trading'),
            CompanyItem('web3', 'https://web3.bamboohr.com/jobs', ScrapeBamboohr, 'https://web3.foundation',
                        'web3'),
            CompanyItem("solana", "https://boards.greenhouse.io/solana", ScrapeGreenhouse,
                        "https://solana.com", "Blockchain"),
            CompanyItem('mobilecoin', 'https://boards.greenhouse.io/mobilecoin', ScrapeGreenhouse,
                        'https://mobilecoin.com', 'Blockchain'),
            CompanyItem('chia', 'https://www.chia.net/careers', ScrapeGreenhouse,
                        'https://www.chia.net', 'Blockchain'),
            CompanyItem("worldcoin", "https://boards.greenhouse.io/worldcoinorg", ScrapeGreenhouse,
                        "https://worldcoin.org", "Blockchain"),
            CompanyItem("edgeandnode", "https://boards.greenhouse.io/edgeandnode", ScrapeGreenhouse,
                        "https://edgeandnode.com", "Infra"),
            CompanyItem("clearmatics", "https://boards.greenhouse.io/clearmatics", ScrapeGreenhouse,
                        "https://www.clearmatics.com", "Protocol"),
            CompanyItem('bitstamp', 'https://apply.workable.com/bitstamp/#jobs', ScrapeWorkable,
                        'https://www.bitstamp.net', 'Exchange'),
            CompanyItem('yugalabs', 'https://boards.greenhouse.io/yugalabs', ScrapeGreenhouse,
                        'https://yuga.com', 'NFT'),
            CompanyItem('cryptofinance', 'https://apply.workable.com/crypto-finance', ScrapeWorkable,
                        'https://www.crypto-finance.com', 'Exchange'),
            CompanyItem('bitget', 'https://apply.workable.com/bitget', ScrapeWorkable, 'https://www.bitget.com/en',
                        'Exchange'),
            CompanyItem('paraswap', 'https://apply.workable.com/paraswap', ScrapeWorkable,
                        'https://www.paraswap.io', 'Web3 DeFi aggregator'),
            CompanyItem('stakefish', 'https://apply.workable.com/stakefish',
                        ScrapeWorkable, 'https://stake.fish', 'Web3 ETH staking')
            ]


def get_company(name) -> CompanyItem:
    company_list = get_company_list()
    companies = list(filter(lambda jd: jd.company_name == name, company_list))
    if len(companies) > 1:
        raise NameError(f'Duplicated company name: {name}')
    return companies[0]


def write_companies(file_name):
    result_list = []
    for com in get_company_list():
        company_item = {
            "company_name": com.company_name,
            "company_url": com.company_url,
            "jobs_url": com.jobs_url,
        }
        result_list.append(company_item)
    print(f'[COMPANY_LIST] Number of Companies writen {len(result_list)}')
    with open(file_name, 'w') as companies_file:
        json.dump(result_list, companies_file, indent=4)
