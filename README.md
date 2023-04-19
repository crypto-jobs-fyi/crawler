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
Given that you have Python 3.5+ and pip instaleed just run pip install -r requirements.txt
Crawler uses just 1 none standard libs:
- selenium 
- `pip install -r requirements.txt`
Next just run `crawler.py`

## Docker
- `docker build --tag scrap:latest .`
- `docker run --rm -it -v ${PWD}:/data docker.io/library/scrap:latest`

# UI staff
Let's try GitHub pages here: https://yury-dubinin.github.io/crypto-jobs-crawler/
Locally just run `python3 -m http.server 8000` and open `localhost:8000` in your browser.

# What we will watch -> work in progress

wip:
- https://jobs.paradigm.xyz/companies/blur-io
- https://jobs.ashbyhq.com/Paradigm
- https://gnosis.jobs.personio.com
- https://nexusmutual.recruitee.com
- https://metrika.recruitee.com
- https://jobs.ashbyhq.com/dune
- https://jobs.ashbyhq.com/cryptio
- https://www.trmlabs.com/careers#open-roles
- https://kiln.crew.work/jobs
- https://ratedlabs.notion.site/Open-Roles-at-Rated
- https://zenith-caboc-8a4.notion.site/Join-Llama-ad66be1cb28541f5b5346aa37d192b79
- https://bullish.wd3.myworkdayjobs.com/Bullish
- https://verum.capital/careers
- https://careers.aplo.io
- https://jobs.coinmarketcap.com
- https://www.abra.com/careers
- https://changenow.io/jobs
- https://jobs.bitvavo.com/en/jobs
- https://web3labs.jobs.personio.com
- https://www.gemini.com/careers
- https://nexo.breezy.hr
- https://careers.stacks.org
- https://www.coinbase.com/careers/positions
- https://www.kucoin.com/careers/job-opening
- https://careers.lido.fi/
- https://www.seba.swiss/careers
- https://www.rdx.works/careers#careers
- https://horizenlabs.io/careers/#list-jobs
- https://careers.substrate.io/jobs
- https://join.com/companies/taurusgroup
- https://changenow.io/jobs
- https://chainsafe.github.io/protocol
- https://jobs.ashbyhq.com/StationLabs
- https://www.sofi.com/careers
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?page=1&pageSize=50
- https://www.openzeppelin.com/jobs
- https://tusd.io/careers/#workwithus
- https://apply.workable.com/walletconnect/
- https://careers.chorus.one/
- https://staking-facilities-gmbh.jobs.personio.com/
- https://jobs.coinfund.io/jobs?page=2
- https://join-incept.super.site/
- https://rhino.fi/careers/
- https://safe-global.breezy.hr/
- https://nascent-xyz.breezy.hr/
- https://angel.co/company/chainflip/jobs
- https://coin98.bamboohr.com/careers
- https://enjin.io/opportunities#positions
- https://bitflyer.com/en-jp/recruit#positions
- https://dydx.exchange/careers#roles
- https://careers.lmax.com
- https://apply.workable.com/prepo
- https://livepeer.org/jobs
- https://boards.greenhouse.io/orderlynetwork
- https://jobs.lever.co/sprucesystems
- https://apply.workable.com/stakefish
- https://jobs.lever.co/kava
- https://www.blockchains.com/careers/#board
- https://phantom.app/jobs
- https://fantom.foundation/careers
- https://apply.workable.com/oasisapp
- https://careers.smartrecruiters.com/Bitoasis
- https://www.coincover.com/careers
- https://jobs.ashbyhq.com/Blockworks
- https://boards.greenhouse.io/bitfury
- https://careers.koinly.io/jobs
- https://jobs.lever.co/AQX
- https://voltz.notion.site/Voltz-Labs-is-Hiring-f1a8857cb7b24d43968cfd735f52292a
- https://hop.exchange/careers

not only crypto:

- https://boards.greenhouse.io/brave

not yet crypto:

- https://boards.greenhouse.io/papaya
- https://boards.greenhouse.io/ramp

to be fixed:
