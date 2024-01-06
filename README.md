# crypto-jobs-crawler
The idea is to build a dashboard with crypto jobs plus some index number to track industry health. Plus you can search for a job as well :)

# support the project
If you find this project useful please donate ETH/ERC-20 to [0x589a0d87d600a6c6faa34c491c9e779f434bc51d](https://etherscan.io/address/0x589a0d87d600a6c6faa34c491c9e779f434bc51d)

# roadmap
- automate scraping positions from most popular HR platforms
- enable simple way of displaying these positions in browser
- enable storage of data as it needed for index calculations
- build better UI with simple search feature
- ...

# how to use?
Given that you have Python 3.5+ and pip installed just run pip install -r requirements.txt
Crawler uses just 1 none standard libs:
- selenium 
- `pip install -r requirements.txt`
Next just run `crawler.py`

## Docker
- `docker build --tag scrap:latest .`
- `docker run --rm -it -v ${PWD}:/data docker.io/library/scrap:latest`

# UI staff
Let's try GitHub pages here: https://crypto-jobs-fyi.github.io/web/
Locally just run `python3 -m http.server 8000` and open `localhost:8000` in your browser.

# What we will watch -> work in progress

wip:
- https://support.bitmart.com/hc/en-us/categories/10942109789723-Career-Opportunities
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?page=1&pageSize=50
- https://www.coinex.com/en/careers/department
- https://careers.sandbox.game/
- https://www.pagoda.co/careers
- https://jobs.paradigm.xyz/companies/blur-io
- https://gnosis.jobs.personio.com
- https://nexusmutual.recruitee.com
- https://metrika.recruitee.com
- https://careers.altlayer.io
- https://ratedlabs.notion.site/Open-Roles-at-Rated
- https://mantanetwork.notion.site/Careers-at-Manta-Ray-Labs-ee51d87f063447b197c5f201f69c9f1b
- https://zenith-caboc-8a4.notion.site/Join-Llama-ad66be1cb28541f5b5346aa37d192b79
- https://bullish.wd3.myworkdayjobs.com/Bullish
- https://verum.capital/careers
- https://careers.aplo.io
- https://jobs.coinmarketcap.com
- https://www.abra.com/careers
- https://changenow.io/jobs
- https://jobs.bitvavo.com/en/jobs
- https://web3labs.jobs.personio.com
- https://nexo.breezy.hr
- https://koii-network.breezy.hr
- https://transak-inc.breezy.hr
- https://careers.stacks.org
- https://www.kucoin.com/careers/job-opening
- https://www.seba.swiss/careers
- https://www.rdx.works/careers#careers
- https://horizenlabs.io/careers/#list-jobs
- https://careers.substrate.io/jobs
- https://join.com/companies/taurusgroup
- https://changenow.io/jobs
- https://chainsafe.github.io/protocol
- https://www.sofi.com/careers
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?page=1&pageSize=50
- https://www.openzeppelin.com/jobs
- https://careers.chorus.one/
- https://staking-facilities-gmbh.jobs.personio.com/
- https://jobs.coinfund.io/jobs?page=2
- https://join-incept.super.site/
- https://rhino.fi/careers/
- https://nascent-xyz.breezy.hr/
- https://angel.co/company/chainflip/jobs
- https://coin98.bamboohr.com/careers
- https://bitflyer.com/en-jp/recruit#positions
- https://livepeer.org/jobs
- https://jobs.lever.co/kava
- https://www.blockchains.com/careers/#board
- https://join.com/companies/21-finance
- https://fantom.foundation/careers
- https://careers.smartrecruiters.com/Bitoasis
- https://www.coincover.com/careers
- https://careers.koinly.io/jobs
- https://voltz.notion.site/Voltz-Labs-is-Hiring-f1a8857cb7b24d43968cfd735f52292a
- https://hop.exchange/careers
- https://careers.bitrefill.com/jobs/
- https://bankless.pallet.com/jobs
- https://www.certora.com/#careers
- https://istari.vision/en/career/
- https://celestia.pallet.com/jobs
- https://gamescoin.jobs.personio.de/
- https://jobs.hiro.cash/
- https://apply.workable.com/interlay/
- https://composable-finance.jobs.personio.com/
- https://www.karpatkey.com/jobs
- https://jobs.outlierventures.io/jobs
- https://coda.io/@josh-rosenblatt-co-create/careers-at-co-create
- https://jobs.settlemint.com/
- https://interchain-gmbh.breezy.hr/
- https://zondacrypto.softgarden.io/en/vacancies
- https://lightcurve.jobs.personio.de/
- https://horizenlabs.io/careers/
- https://l2beat.notion.site/We-are-hiring-Work-at-L2BEAT-e4e637265ae94c5db7dfa2de336b940f
- https://bwarelabs.mingle.ro/en/apply
- https://github.com/tvl-labs/job-board/blob/main/engineering/protocol_engineer.md
- https://wellfound.com/company/redstonefinance/jobs
- https://stake-capital-group.breezy.hr/
- https://polygon.technology/ecosystem-jobs
- https://jobs.dragonfly.xyz/jobs 
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?department=[1110473]
- https://www.ethswarm.org/jobs
- https://cash.app/careers
- https://join.com/companies/peaq
- https://strike.me/careers/
- https://edxmarkets.com/about/careers/
- https://bloxstaking.breezy.hr/
- https://zero-hash.breezy.hr/
- https://trendspider.freshteam.com/jobs
- https://careers.onetrading.com/jobs
- https://bitso.com/jobs
- https://sologenic-development-foundation-limited.breezy.hr/
- https://www.lightspark.com/careers
- https://www.talos.com/working/open-roles
- https://www.coinomi.com/careers
- https://apply.workable.com/apollolabs  https://apollo.xyz/
- https://apply.workable.com/summerfi/#jobs https://summer.fi/
- https://cryptotaxcalculator.io/us/jobs/
- https://careers.transak.com/
- https://base.org/jobs
- https://lavanet.applytojob.com/apply/
- https://www.kamu.dev/jobs/
- https://jobs.zama.ai/departments/tfhe-rs
- https://www.soliduslabs.com/careers#open-positions
- https://www.ambergroup.io/people?location=All&jobType=All
- https://apply.workable.com/ferrum/
- https://lightcurve.jobs.personio.de/?language=en


not only crypto:

- https://careers.smartrecruiters.com/MicroStrategy1
- https://jobs.lever.co/Hume - https://wearehume.com

not yet crypto:

- https://boards.greenhouse.io/papaya
- https://boards.greenhouse.io/ramp
- https://jobs.lever.co/pigment
- https://jobs.lever.co/neednova
- https://plaid.com/careers/openings

to be fixed:
