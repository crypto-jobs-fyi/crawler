import json

from src.company_item import CompanyItem
from src.scrape_enjin import ScrapeEnjin
from src.scrape_lever import ScrapeLever
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_lmax import ScrapeLmax
from src.scrape_smartrecruiters import ScrapeSmartrecruiters
from src.scrape_recruitee import ScrapeRecruitee
from src.scrape_bamboohr import ScrapeBamboohr
from src.scrape_consensys import ScrapeConsensys
from src.scrape_ripple import ScrapeRipple
from src.scrape_tusd import ScrapeTusd
from src.scrape_workable import ScrapeWorkable
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_paxos import ScrapePaxos
from src.scrape_coinbase import ScrapeCoinbase
from src.scrape_gemini import ScrapeGemini
from src.scrape_workday import ScrapeWorkday
from src.scrape_base import ScrapeBase
from src.scrape_phantom import ScrapePhantom
from src.scrape_tether import ScrapeTether


def get_company_list() -> [CompanyItem]:
    return [CompanyItem('base', 'https://base.org/jobs', ScrapeBase, 'https://base.org', 'Web3 Infra'),
            CompanyItem("binance", "https://jobs.lever.co/binance", ScrapeLever,
                        "https://www.binance.com", "The Exchange"),
            CompanyItem('lmax', 'https://careers.lmax.com/job-openings', ScrapeLmax,
                        'https://www.lmax.com', 'Web3 browser'),
            CompanyItem("kraken", "https://jobs.ashbyhq.com/kraken.com", ScrapeAshbyhq, "https://kraken.com", "Exchange"),
            CompanyItem('lido', 'https://jobs.ashbyhq.com/PML', ScrapeAshbyhq,
                        'https://lido.fi', 'Web3 Staking'),
            CompanyItem('moonpay', 'https://moonpay.wd1.myworkdayjobs.com/en-US/GTI', ScrapeWorkday,
                        'https://www.moonpay.com', 'Web3 Payments'),
            CompanyItem('phantom', 'https://phantom.app/jobs', ScrapePhantom,
                        'https://gate.io', 'Web3 Exchange'),
            CompanyItem('obol-tech', 'https://jobs.lever.co/obol-tech', ScrapeLever,
                        'https://obol.tech', 'ETH Distributed Staking'),
            CompanyItem('arbitrumfoundation', 'https://jobs.lever.co/arbitrumfoundation', ScrapeLever,
                        'https://arbitrum.foundation', 'Layer 2'),
            CompanyItem("chainlink", "https://jobs.lever.co/chainlink", ScrapeLever, "https://chain.link",
                        "L1 Blockchain"),
            CompanyItem('aragon', 'https://jobs.lever.co/aragon', ScrapeLever,
                        'https://aragon.org', 'Web3 DAO launcher'),
            CompanyItem('ondofinance', 'https://jobs.lever.co/ondofinance', ScrapeLever, 'https://ondo.finance',
                        'Web3 yield'),
            CompanyItem('omni-network', 'https://jobs.lever.co/omni-network', ScrapeLever,
                        'https://omni.network', 'Web3 inter-chain'),
            CompanyItem('Tenderly', 'https://jobs.lever.co/Tenderly', ScrapeLever,
                        'https://tenderly.co', 'Web3 Infra'),
            CompanyItem('injectivelabs', 'https://jobs.lever.co/injectivelabs', ScrapeLever,
                        'https://injectivelabs.org', 'Web3 Infra'),
            CompanyItem('nomic.foundation', 'https://jobs.ashbyhq.com/nomic.foundation', ScrapeAshbyhq,
                        'https://nomic.foundation', 'Web3 Infra'),
            CompanyItem('ethglobal', 'https://jobs.ashbyhq.com/ethglobal', ScrapeAshbyhq, 'https://ethglobal.com',
                        'Community'),
            CompanyItem('li.fi', 'https://jobs.ashbyhq.com/li.fi', ScrapeAshbyhq,
                        'https://li.fi', 'DeFi Liquidity'),
            CompanyItem('Caldera', 'https://jobs.ashbyhq.com/Caldera', ScrapeAshbyhq, 'https://www.caldera.xyz',
                        'L2 Rollups'),
            CompanyItem('blox-route', 'https://jobs.lever.co/blox-route', ScrapeLever,
                        'https://bloxroute.com', 'Web3 MEV DeFi infra'),
            CompanyItem('multiversx', 'https://jobs.lever.co/multiversx', ScrapeLever, 'https://multiversx.com',
                        'Blockchain'),
            CompanyItem('sprucesystems', 'https://jobs.lever.co/sprucesystems', ScrapeLever, 'https://spruceid.com',
                        'Web3 ID'),
            CompanyItem('BlockSwap', 'https://jobs.lever.co/BlockSwap', ScrapeLever, 'https://www.blockswap.network',
                        'Infra'),
            CompanyItem('scroll', 'https://jobs.lever.co/ScrollFoundation', ScrapeLever,
                        'https://scroll.io', 'Web3 Infra'),
            CompanyItem('impossiblecloud', 'https://jobs.lever.co/impossiblecloud', ScrapeLever,
                        'https://www.impossiblecloud.com', 'Web3 Infra'),
            CompanyItem('with-foundation', 'https://jobs.lever.co/with-foundation', ScrapeLever,
                        'https://foundation.app', 'Web3 NFT'),
            CompanyItem('Metatheory', 'https://jobs.lever.co/Metatheory', ScrapeLever,
                        'https://www.duskbreakers.gg', 'Web3 game'),
            CompanyItem('axiomzen', 'https://jobs.lever.co/axiomzen', ScrapeLever, 'https://www.axiomzen.com', 'Web3'),
            CompanyItem('fuellabs', 'https://jobs.lever.co/fuellabs', ScrapeLever, 'https://www.fuel.network',
                        'Blockchain'),
            CompanyItem('HQxyz', 'https://jobs.lever.co/HQxyz', ScrapeLever,
                        'https://www.hq.xyz', 'Web3 Back Office'),
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
            CompanyItem('fortress', 'https://jobs.lever.co/fortress', ScrapeLever,
                        'https://fortress.io', 'Web3 Custody'),
            CompanyItem("storyprotocol", "https://jobs.lever.co/storyprotocol", ScrapeLever,
                        "https://www.storyprotocol.xyz", "Protocol"),
            CompanyItem("ethereumfoundation", "https://jobs.lever.co/ethereumfoundation", ScrapeLever,
                        "https://ethereum.org", "L1 Blockchain"),
            CompanyItem("aave", "https://jobs.eu.lever.co/avara", ScrapeLever, "https://avara.xyz", "Web3 Protocol"),
            CompanyItem("crypto", "https://jobs.lever.co/crypto", ScrapeLever, "https://crypto.com", "Exchange"),
            CompanyItem("Luxor", "https://jobs.lever.co/LuxorTechnology", ScrapeLever, "https://www.luxor.tech",
                        "Mining"),
            CompanyItem("anchorage", "https://jobs.lever.co/anchorage", ScrapeLever, "https://www.anchorage.com",
                        "Trading"),
            CompanyItem("biconomy", "https://jobs.lever.co/biconomy", ScrapeLever, "https://www.biconomy.io",
                        "Infra"),
            CompanyItem('enso', 'https://jobs.lever.co/Enso', ScrapeLever, 'https://www.enso.finance', 'DeFi'),
            CompanyItem("Polygon", "https://jobs.lever.co/Polygon", ScrapeLever, "https://polygon.technology",
                        "L2 Blockchain"),
            CompanyItem('centrifuge', 'https://jobs.lever.co/centrifuge', ScrapeLever, 'https://centrifuge.io',
                        'Web3 yield'),
            CompanyItem("tokenmetrics", "https://jobs.lever.co/tokenmetrics", ScrapeLever,
                        "https://www.tokenmetrics.com", "Information"),
            CompanyItem("offchainlabs", "https://jobs.lever.co/offchainlabs", ScrapeLever,
                        "https://offchainlabs.com", "Protocol"),
            CompanyItem("subspacelabs", "https://jobs.lever.co/subspacelabs", ScrapeLever,
                        "https://subspace.network", "Blockchain Infra"),
            CompanyItem('3boxlabs', 'https://jobs.lever.co/3box', ScrapeLever, 'https://3boxlabs.com',
                        'Infra'),
            CompanyItem("ramp.network", "https://boards.eu.greenhouse.io/rampnetwork", ScrapeGreenhouse,
                        "https://ramp.network", "Payments"),
            CompanyItem("eiger", "https://boards.eu.greenhouse.io/eiger", ScrapeGreenhouse,
                        "https://www.eiger.co", "Web3 development"),
            CompanyItem('risklabs', 'https://jobs.lever.co/risklabs', ScrapeLever, 'https://risklabs.foundation',
                        'Protocol'),
            CompanyItem('celestia', 'https://jobs.lever.co/celestia', ScrapeLever, 'https://celestia.org',
                        'Modular Blockchain'),
            CompanyItem('polymerlabs', 'https://jobs.lever.co/polymerlabs', ScrapeLever, 'https://www.polymerlabs.org',
                        'Modular Blockchain'),
            CompanyItem('swellnetwork', 'https://jobs.lever.co/swellnetwork.io', ScrapeLever,
                        'https://www.swellnetwork.io', 'Web3 ETH LST'),
            CompanyItem('royal', 'https://jobs.lever.co/Royal', ScrapeLever, 'https://royal.io', 'Web3 + Music'),
            CompanyItem('gauntlet', 'https://jobs.lever.co/gauntlet', ScrapeLever, 'https://gauntlet.network',
                        'Web3 + Financial Modelling'),
            CompanyItem('machinefilab', 'https://jobs.lever.co/machinefilab', ScrapeLever, 'https://machinefi.com/lab',
                        'Web3 yield'),
            CompanyItem('clabs', 'https://jobs.lever.co/clabs', ScrapeLever, 'https://clabs.co',
                        'Web3 Celo'),
            CompanyItem('gate.io', 'https://jobs.lever.co/gate.io', ScrapeLever,
                        'https://gate.io', 'Web3 Exchange'),
            CompanyItem('auroralabs', 'https://jobs.lever.co/aurora-dev', ScrapeLever,
                        'https://auroralabs.dev', 'EVM blockchain'),
            CompanyItem("ledger", "https://jobs.lever.co/ledger", ScrapeLever, "https://www.ledger.com", "Wallet"),
            CompanyItem("immutable", "https://jobs.lever.co/immutable", ScrapeLever, "https://www.immutable.com",
                        "NFT"),
            CompanyItem("web3auth", "https://jobs.lever.co/TorusLabs", ScrapeLever, "https://web3auth.io", "Auth"),
            CompanyItem("cere-network", "https://jobs.lever.co/cere-network", ScrapeLever, "https://cere.network",
                        "Infra"),
            CompanyItem('matterlabs', 'https://jobs.eu.lever.co/matterlabs', ScrapeLever, 'https://matter-labs.io',
                        'Protocol'),
            CompanyItem("monad", "https://boards.greenhouse.io/monad", ScrapeGreenhouse, "https://www.monad.xyz",
                        "L1 EVM blockchain"),
            CompanyItem("iftother", "https://boards.greenhouse.io/iftother", ScrapeGreenhouse,
                        "https://free.technology", 'WEB3'),
            CompanyItem("wyndlabs", "https://boards.greenhouse.io/wyndlabs", ScrapeGreenhouse,
                        "https://www.wyndlabs.ai", 'WEB3 AI'),
            CompanyItem('expopulus', 'https://jobs.lever.co/Expopulus', ScrapeLever,
                        'https://expopulus.com', 'Web3 game'),
            CompanyItem("coinlist", "https://apply.workable.com/coinlist", ScrapeWorkable, "https://coinlist.co",
                        "Web3 Exchange Launchpad"),
            CompanyItem('animocabrands', 'https://jobs.lever.co/animocabrands', ScrapeLever,
                        'https://www.animocabrands.com', 'Web3 Gaming'),
            CompanyItem('toku', 'https://jobs.lever.co/toku', ScrapeLever,
                        'https://www.toku.com', 'Web3 Tokens and Tax'),
            CompanyItem("hiro", "https://boards.greenhouse.io/hiro", ScrapeGreenhouse, "https://www.hiro.so", "Infra"),
            CompanyItem('AQX', 'https://jobs.lever.co/presto', ScrapeLever, 'https://aqx.com', 'Exchange and Web3'),
            CompanyItem('ultra', 'https://jobs.lever.co/ultra', ScrapeLever,
                        'https://ultra.io', 'Web3 Gaming'),
            CompanyItem('glassnode', 'https://jobs.lever.co/glassnode', ScrapeLever,
                        'https://glassnode.com', 'Web3 Info'),
            CompanyItem('coingecko', 'https://jobs.lever.co/coingecko', ScrapeLever,
                        'https://www.coingecko.com', 'Web3 Info'),
            CompanyItem('emergentx', 'https://jobs.lever.co/emergentx', ScrapeLever,
                        'https://www.emergentx.org', 'Web3 tokenization'),
            CompanyItem('connext-network', 'https://jobs.lever.co/connext-network', ScrapeLever,
                        'https://www.connext.network', 'Web3 Infra'),
            CompanyItem('ethenalabs', 'https://jobs.lever.co/ethenalabs', ScrapeLever,
                        'https://www.ethena.fi', 'Web3 bonds'),
            CompanyItem('SeiLabs', 'https://jobs.lever.co/SeiLabs', ScrapeLever,
                        'https://www.sei.io', 'L1 EVM blockchain'),
            CompanyItem('theblock', 'https://jobs.lever.co/theblockcrypto', ScrapeLever,
                        'https://www.theblock.co', 'Web3 Info'),
            CompanyItem('bitwise', 'https://jobs.lever.co/bitwiseinvestments', ScrapeLever,
                        'https://bitwiseinvestments.com', 'Asset Management'),
            CompanyItem('grayscaleinvestments', 'https://boards.greenhouse.io/grayscaleinvestments', ScrapeGreenhouse,
                        'https://grayscale.com', 'Web3 Asset Manager'),
            CompanyItem('dydx', 'https://boards.greenhouse.io/dydx', ScrapeGreenhouse,
                        'https://dydx.exchange', 'Web3 Exchange'),
            CompanyItem('xlabs', 'https://jobs.ashbyhq.com/Xlabs', ScrapeAshbyhq,
                        'https://www.xlabs.xyz', 'Web3 Infra'),
            CompanyItem('movementlabs', 'https://jobs.ashbyhq.com/movementlabs', ScrapeAshbyhq,
                        'https://movementlabs.xyz',
                        'Modular chain'),
            CompanyItem('succinct', 'https://jobs.ashbyhq.com/succinct', ScrapeAshbyhq, 'https://succinct.xyz',
                        'Zero-knowledge proofs'),
            CompanyItem("jumpcrypto", "https://boards.greenhouse.io/jumpcrypto", ScrapeGreenhouse,
                        "https://jumpcrypto.com", "Web3 Infra"),
            CompanyItem("0x", "https://boards.greenhouse.io/0x", ScrapeGreenhouse, "https://0x.org",
                        "L2 Blockchain"),
            CompanyItem("ritual", "https://boards.greenhouse.io/ritual", ScrapeGreenhouse,
                        "https://ritual.net", 'WEB3 AI'),
            CompanyItem('econetwork', 'https://boards.greenhouse.io/econetwork', ScrapeGreenhouse,
                        'https://eco.com', 'Web3 wallet'),
            CompanyItem('magic', 'https://boards.greenhouse.io/magic', ScrapeGreenhouse, 'https://magic.link',
                        'Web3 Wallets'),
            CompanyItem("chainstack", "https://chainstack.bamboohr.com/careers", ScrapeBamboohr,
                        "https://chainstack.com", "Infra"),
            CompanyItem('outlierventures', 'https://outlierventures.bamboohr.com/careers', ScrapeBamboohr,
                        'https://outlierventures.io', 'Web3 Ventures'),
            CompanyItem('dappradar', 'https://dappradar.bamboohr.com/careers', ScrapeBamboohr,
                        'https://dappradar.com', 'Exchange & NFT'),
            CompanyItem("coinmarketcap", "https://careers.smartrecruiters.com/B6/coinmarketcap",
                        ScrapeSmartrecruiters, "https://coinmarketcap.com", "Information"),
            CompanyItem('evmos', 'https://boards.eu.greenhouse.io/evmos', ScrapeGreenhouse, 'https://evmos.org',
                        'Cross-Chain Connectivity'),
            CompanyItem('pyth', 'https://boards.greenhouse.io/pythdataassociation', ScrapeGreenhouse,
                        'https://pyth.network', 'Web3 Data'),
            CompanyItem('orderlynetwork', 'https://boards.greenhouse.io/orderlynetwork', ScrapeGreenhouse,
                        'https://orderly.network', 'Exchange'),
            CompanyItem('shardeum', 'https://boards.greenhouse.io/shardeumfoundation', ScrapeGreenhouse,
                        'https://shardeum.org', 'Web3 L1'),
            CompanyItem("paxos",
                        "https://paxos.com/job-posts/?_sft_department=engineering-data,finance-accounting,hr-talent,information-technology,legal,operations,product-management,risk-compliance&_sft_office=us",
                        ScrapePaxos, "https://paxos.com", "Stable Coin"),
            CompanyItem("zora", "https://boards.greenhouse.io/zora", ScrapeGreenhouse, "https://zora.co", "NFT"),
            CompanyItem('bitfury', 'https://boards.greenhouse.io/bitfury', ScrapeGreenhouse, 'https://bitfury.com',
                        'Web3'),
            CompanyItem("blockchain", "https://boards.greenhouse.io/blockchain", ScrapeGreenhouse,
                        "https://www.blockchain.com", "Exchange"),
            CompanyItem('osl', 'https://bcgroup.bamboohr.com/careers', ScrapeBamboohr,
                        'https://osl.com', 'Web3 Custody Exchange'),
            CompanyItem("cexio", "https://cexio.bamboohr.com/jobs", ScrapeBamboohr, "https://cex.io", "Exchange"),
            CompanyItem("circle", "https://boards.greenhouse.io/circle", ScrapeGreenhouse, "https://circle.com",
                        "Stable Coin"),
            CompanyItem("OKX", "https://boards.greenhouse.io/OKX", ScrapeGreenhouse, "https://okx.com",
                        "Exchange"),
            CompanyItem("bitmex", "https://boards.greenhouse.io/bitmex", ScrapeGreenhouse, "https://bitmex.com",
                        "Exchange"),
            CompanyItem("bitgo", "https://boards.greenhouse.io/bitgo", ScrapeGreenhouse, "https://bitgo.com",
                        "Exchange"),
            CompanyItem("bitpanda", "https://boards.eu.greenhouse.io/bitpanda", ScrapeGreenhouse,
                        "https://bitpanda.com", "Exchange"),
            CompanyItem("uniswaplabs", "https://boards.greenhouse.io/uniswaplabs", ScrapeGreenhouse,
                        "https://uniswap.org", "Exchange Protocol"),
            CompanyItem('osmosisdex', 'https://boards.greenhouse.io/osmosisdex', ScrapeGreenhouse,
                        'https://osmosis.zone', 'Exchange'),
            CompanyItem('penumbralabs', 'https://boards.greenhouse.io/penumbralabs', ScrapeGreenhouse,
                        'https://eco.com', 'Web3 trading'),
            CompanyItem("blockdaemon", "https://boards.greenhouse.io/blockdaemon", ScrapeGreenhouse,
                        "https://www.blockdaemon.com", "Staking & Infra"),
            CompanyItem("figment", "https://boards.greenhouse.io/figment", ScrapeGreenhouse,
                        "https://www.figment.io", "Staking & Infra"),
            CompanyItem("OpenSea", "https://jobs.ashbyhq.com/OpenSea", ScrapeAshbyhq, "https://opensea.io", "NFT"),
            CompanyItem('center', 'https://jobs.ashbyhq.com/center', ScrapeAshbyhq,
                        'https://center.app', 'Web3 NFT Data'),
            CompanyItem('linera.io', 'https://jobs.ashbyhq.com/linera.io', ScrapeAshbyhq,
                        'https://linera.io', 'Layer-1 blockchain'),
            CompanyItem('shadow', 'https://jobs.ashbyhq.com/shadow', ScrapeAshbyhq,
                        'https://www.shadow.xyz', 'Web3 Infra'),
            CompanyItem('cointracker', 'https://jobs.ashbyhq.com/cointracker', ScrapeAshbyhq,
                        'https://www.cointracker.io', 'Web3 Back Office'),
            CompanyItem('Bastion', 'https://jobs.ashbyhq.com/Bastion', ScrapeAshbyhq,
                        'https://www.bastion.com', 'Web3 Infra and Wallet'),
            CompanyItem('Sui.Foundation', 'https://jobs.ashbyhq.com/Sui%20Foundation', ScrapeAshbyhq,
                        'https://sui.io', 'Web3 blockchain'),
            CompanyItem('dourolabs', 'https://jobs.ashbyhq.com/dourolabs.xyz', ScrapeAshbyhq,
                        'https://dourolabs.xyz', 'Web3 Data(Pyth)'),
            CompanyItem('StationLabs', 'https://jobs.ashbyhq.com/StationLabs', ScrapeAshbyhq,
                        'https://www.station.express', 'Web3 infra'),
            CompanyItem('rain', 'https://jobs.ashbyhq.com/rain', ScrapeAshbyhq, 'https://www.raincards.xyz',
                        'Web3 cards'),
            CompanyItem('mystenlabs', 'https://jobs.ashbyhq.com/mystenlabs', ScrapeAshbyhq,
                        'https://mystenlabs.com', 'Web3 Infra'),
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
            CompanyItem("solanafoundation", "https://jobs.ashbyhq.com/Solana%20Foundation", ScrapeAshbyhq,
                        "https://solana.org", "L1 Blockchain"),
            CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhq, 'https://syndica.io',
                        'Infrastructure'),
            CompanyItem('Blockworks', 'https://jobs.ashbyhq.com/Blockworks', ScrapeAshbyhq,
                        'https://blockworks.co', 'Web3 News'),
            CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhq,
                        'https://ellipsislabs.xyz', 'Trading Protocol'),
            CompanyItem('safe.global', 'https://jobs.ashbyhq.com/safe.global', ScrapeAshbyhq,
                        'https://safe.global', 'Web3 custody'),
            CompanyItem('cryptio', 'https://jobs.ashbyhq.com/cryptio', ScrapeAshbyhq,
                        'https://cryptio.co', 'Web3 Back Office'),
            CompanyItem('Artemisxyz', 'https://jobs.ashbyhq.com/Artemisxyz', ScrapeAshbyhq,
                        'https://www.artemis.xyz', 'Web3 Data'),
            CompanyItem('Boost', 'https://jobs.ashbyhq.com/Boost', ScrapeAshbyhq,
                        'https://Boost.xyz', 'Web3 gaming'),
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
            CompanyItem("chainalysis", "https://jobs.ashbyhq.com/chainalysis-careers", ScrapeAshbyhq,
                        "https://www.chainalysis.com", "Crypto Research"),
            CompanyItem("magiceden", "https://boards.greenhouse.io/magiceden", ScrapeGreenhouse,
                        "https://www.magiceden.io", "NFT"),
            CompanyItem("aztec", "https://boards.eu.greenhouse.io/aztec", ScrapeGreenhouse,
                        "https://aztec.network", "Protocol"),
            CompanyItem('near', 'https://boards.greenhouse.io/near', ScrapeGreenhouse,
                        'https://near.org', 'Web3 Protocol'),
            CompanyItem("nethermind", "https://boards.eu.greenhouse.io/nethermind", ScrapeGreenhouse,
                        "https://nethermind.io", "Crypto software"),
            CompanyItem("dfinity", "https://boards.greenhouse.io/dfinity", ScrapeGreenhouse, "https://dfinity.org",
                        "L1 Blockchain"),
            CompanyItem('stellar', 'https://boards.greenhouse.io/stellar', ScrapeGreenhouse,
                        'https://stellar.org', 'Blockchain'),
            CompanyItem("parity", "https://boards.greenhouse.io/parity", ScrapeGreenhouse, "https://www.parity.io",
                        "Infra"),
            CompanyItem("optimism", "https://boards.greenhouse.io/optimismunlimited", ScrapeGreenhouse,
                        "https://www.optimism.io", "L2 protocol"),
            CompanyItem('coinmetrics', 'https://boards.greenhouse.io/coinmetrics', ScrapeGreenhouse,
                        'https://coinmetrics.io', 'Web3 Data'),
            CompanyItem("oplabs", "https://boards.greenhouse.io/oplabs", ScrapeGreenhouse, "https://www.oplabs.co",
                        "L2 protocol"),
            CompanyItem('goldsky', 'https://boards.greenhouse.io/goldsky', ScrapeGreenhouse,
                        'https://goldsky.com', 'Web3 Data'),
            CompanyItem('walletconnect', 'https://apply.workable.com/walletconnect', ScrapeWorkable,
                        'https://walletconnect.com', 'Web3 Wallet Infra'),
            CompanyItem('prepo', 'https://apply.workable.com/prepo', ScrapeWorkable,
                        'https://prepo.io', 'Web3 pre-IPO trading'),
            CompanyItem('io-global', 'https://apply.workable.com/io-global/#jobs', ScrapeWorkable,
                        'https://iohk.io', 'Web3 Blockchain'),
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
                        "https://www.avalabs.org", "L1 Blockchain"),
            CompanyItem("aptoslabs", "https://boards.greenhouse.io/aptoslabs", ScrapeGreenhouse,
                        "https://aptoslabs.com", "L1 Blockchain"),
            CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                        'https://www.iofinnet.com', 'Custody'),
            CompanyItem('iyield', 'https://iyield.bamboohr.com/careers', ScrapeBamboohr, 'https://iyield.com',
                        'Web3 Fin Planning'),
            CompanyItem('almanak', 'https://apply.workable.com/almanak-blockchain-labs-ag', ScrapeWorkable,
                        'https://almanak.co', 'Web3 Simulator'),
            CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhq, 'https://dune.com',
                        'Web3 data'),
            CompanyItem('blast', 'https://jobs.ashbyhq.com/blast-io', ScrapeAshbyhq, 'https://blast.io',
                        'L2'),
            CompanyItem('windranger', 'https://jobs.ashbyhq.com/windranger', ScrapeAshbyhq,
                        'https://windranger.io', 'DeFi Development'),
            CompanyItem("filecoinfoundation", "https://boards.greenhouse.io/filecoinfoundation", ScrapeGreenhouse,
                        "https://fil.org", "L1 Blockchain"),
            CompanyItem('foundrydigital', 'https://boards.greenhouse.io/foundrydigital', ScrapeGreenhouse,
                        'https://foundrydigital.com', 'Web3 Infra'),
            CompanyItem('immunefi', 'https://boards.greenhouse.io/immunefi', ScrapeGreenhouse, 'https://immunefi.com',
                        'Bug bounty platform'),
            CompanyItem('wirex', 'https://wirex.bamboohr.com/careers', ScrapeBamboohr, 'https://wirexapp.com',
                        'Web3 card'),
            CompanyItem('protocollabs', 'https://boards.greenhouse.io/protocollabs', ScrapeGreenhouse,
                        'https://protocol.ai/about',
                        'Web3 IPFS research platform'),
            CompanyItem('trmlabs', 'https://www.trmlabs.com/careers#open-roles', ScrapeGreenhouse,
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
            CompanyItem("ankr", "https://boards.greenhouse.io/ankrnetwork", ScrapeGreenhouse,
                        "https://www.ankr.com", "Web3 Staking Protocol"),
            CompanyItem("chainsafesystems", "https://boards.greenhouse.io/chainsafesystems", ScrapeGreenhouse,
                        "https://chainsafe.io", "Infra"),
            CompanyItem("ripple", "https://ripple.com/careers/all-jobs", ScrapeRipple, "https://ripple.com",
                        "L1 Blockchain"),
            CompanyItem("kadena", "https://boards.greenhouse.io/kadenallc", ScrapeGreenhouse, "https://kadena.io",
                        "L1 Blockchain"),
            CompanyItem("eigenlabs", "https://boards.greenhouse.io/eigenlabs", ScrapeGreenhouse,
                        "https://www.eigenlayer.xyz", "Infra"),
            CompanyItem('sygnum', 'https://sygnum.bamboohr.com/careers', ScrapeBamboohr, 'https://www.sygnum.com',
                        'Crypto bank'),
            CompanyItem("galaxydigitalservices", "https://boards.greenhouse.io/galaxydigitalservices",
                        ScrapeGreenhouse, "https://www.galaxy.com", 'Trading'),
            CompanyItem('web3', 'https://web3.bamboohr.com/jobs', ScrapeBamboohr, 'https://web3.foundation',
                        'web3'),
            CompanyItem("solana", "https://boards.greenhouse.io/solana", ScrapeGreenhouse,
                        "https://solana.com", "L1 Blockchain"),
            CompanyItem('mobilecoin', 'https://boards.greenhouse.io/mobilecoin', ScrapeGreenhouse,
                        'https://mobilecoin.com', 'Blockchain'),
            CompanyItem('chia', 'https://www.chia.net/careers', ScrapeGreenhouse,
                        'https://www.chia.net', 'Blockchain'),
            CompanyItem("worldcoin", "https://boards.greenhouse.io/worldcoinorg", ScrapeGreenhouse,
                        "https://worldcoin.org", "L1 Blockchain"),
            CompanyItem("edgeandnode", "https://boards.greenhouse.io/edgeandnode", ScrapeGreenhouse,
                        "https://edgeandnode.com", "Infra"),
            CompanyItem("clearmatics", "https://boards.greenhouse.io/clearmatics", ScrapeGreenhouse,
                        "https://www.clearmatics.com", "Protocol"),
            CompanyItem('yugalabs', 'https://boards.greenhouse.io/yugalabs', ScrapeGreenhouse,
                        'https://yuga.com', 'NFT'),
            CompanyItem('brave', 'https://boards.greenhouse.io/brave', ScrapeGreenhouse,
                        'https://brave.com', 'Web3 browser'),
            CompanyItem('bitstamp', 'https://apply.workable.com/bitstamp/#jobs', ScrapeWorkable,
                        'https://www.bitstamp.net', 'Exchange'),
            CompanyItem('tatum', 'https://apply.workable.com/tatum', ScrapeWorkable,
                        'https://tatum.io', 'Web3 SDK'),
            CompanyItem('cryptofinance', 'https://apply.workable.com/crypto-finance', ScrapeWorkable,
                        'https://www.crypto-finance.com', 'Exchange'),
            CompanyItem('hextrust', 'https://apply.workable.com/hextrust', ScrapeWorkable,
                        'https://www.hextrust.com', 'Web3 Custody'),
            CompanyItem('zodia-custody', 'https://apply.workable.com/zodia-custody', ScrapeWorkable,
                        'https://zodia.io', 'Web3 Custody'),
            CompanyItem('paraswap', 'https://apply.workable.com/paraswap', ScrapeWorkable,
                        'https://www.paraswap.io', 'Web3 DeFi aggregator'),
            CompanyItem('stakefish', 'https://apply.workable.com/stakefish',
                        ScrapeWorkable, 'https://stake.fish', 'Web3 ETH staking'),
            CompanyItem('thetie', 'https://apply.workable.com/thetie/#jobs', ScrapeWorkable,
                        'https://www.thetie.io', 'Web3 DeFi Info'),
            CompanyItem('tusd', 'https://tusd.io/about', ScrapeTusd,
                        'https://tusd.io', 'Web3 Stable-coin'),
            CompanyItem('enjin', 'https://enjin.io/opportunities#positions', ScrapeEnjin,
                        'https://enjin.io', 'Web3 Blockchain'),
            CompanyItem('status', 'https://boards.greenhouse.io/logos', ScrapeGreenhouse,
                        'https://status.app', 'Web3 Messanger'),
            CompanyItem('gemini', 'https://www.gemini.com/careers', ScrapeGemini,
                        'https://www.gemini.com', 'Web3 Exchange'),
            CompanyItem("tether", "https://tether.recruitee.com", ScrapeTether, "https://tether.to/en",
                        "Stable Coin"),
            CompanyItem('mina-foundation', 'https://apply.workable.com/mina-foundation', ScrapeWorkable,
                        'https://www.minafoundation.com', 'ZK blockchain'),
            CompanyItem("consensys", "https://consensys.net/open-roles", ScrapeConsensys, "https://consensys.net",
                        "Infra"),
            CompanyItem('coinbase', 'https://www.coinbase.com/careers/positions', ScrapeCoinbase,
                        'https://www.coinbase.com', 'Web3 Exchange'),
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
