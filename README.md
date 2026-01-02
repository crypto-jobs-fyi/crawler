# crypto-jobs-crawler

A Python-based web crawler designed to scrape job listings from various crypto, AI, and Fintech company websites and Applicant Tracking Systems (ATS).

The goal is to build a dashboard with industry jobs and track industry health through index calculations.

## Supported Platforms (ATS)
The crawler supports major HR platforms including:
- **Greenhouse**
- **Ashby**
- **Lever**
- **Workable**
- **SmartRecruiters**
- **BambooHR**
- **Gem**
- And many custom company-specific scrapers (Coinbase, Ripple, Gemini, etc.)

## Architecture

- **Orchestration**: Entry points like `crawler_ai.py`, `crypto_crawler.py`, and `crawler_tech.py` manage the scraping process.
- **Scrapers**: Modular scraper classes in `src/` inheriting from `ScrapeIt`.
- **Data Models**: `CompanyItem` defines the target company, its jobs URL, and the scraper to use.
- **Automation**: GitHub Actions workflows automate periodic scraping and data updates via Pull Requests.

## How to use?

### Local Setup
1.  **Environment**: Python 3.12+ is recommended.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Run Crawler**:
    ```bash
    python crawler_ai.py
    ```
    *Note: Crawlers run in headless mode by default. To debug visually, disable headless mode in the crawler script.*

### Docker
- `docker build --tag scrap:latest .`
- `docker run --rm -it -v ${PWD}:/data scrap:latest`

## UI
The scraped data is displayed on GitHub Pages: [crypto-jobs-fyi.github.io/web/](https://crypto-jobs-fyi.github.io/web/)
Locally, you can view it by running:
```bash
python3 -m http.server 8000
```

## Development

### Adding a New Company
1.  Identify the ATS used by the company.
2.  Add a `CompanyItem` to the relevant list in `src/company_*_list.py`:
    ```python
    CompanyItem('CompanyName', 'https://jobs.url', Scrapers.GREENHOUSE, 'https://company.url')
    ```

### Creating a Custom Scraper
1.  Create `src/scrape_<name>.py` inheriting from `ScrapeIt`.
2.  Implement `getJobs(self, driver, web_page, company)`.
3.  Register the new scraper in `src/scrapers.py`.

## Roadmap
- [x] Automate scraping from popular HR platforms
- [x] Enable storage of data for index calculations
- [ ] Build better UI with advanced search features
- [ ] Expand coverage to more niche crypto companies

## Support the project
If you find this project useful, please donate ETH/ERC-20 to:
`0x589a0d87d600a6c6faa34c491c9e779f434bc51d`

---

# Work in Progress (WIP) Links
The following companies are targeted for future integration:
- https://support.bitmart.com/hc/en-us/categories/10942109789723-Career-Opportunities
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?page=1&pageSize=50
- https://apply.workable.com/re7-capital/
- https://careers.persistence.one/jobs
- https://www.eotlabs.io/about-us#Vacancy-Section
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
- https://www.abra.com/careers
- https://changenow.io/jobs
- https://jobs.bitvavo.com/en/jobs
- https://web3labs.jobs.personio.com
- https://nexo.breezy.hr
- https://the-graph.breezy.hr
- https://koii-network.breezy.hr
- https://careers.stacks.org
- https://www.kucoin.com/careers
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
- https://bitflyer.com/en-jp/recruit#positions
- https://livepeer.org/jobs
- https://www.blockchains.com/careers/#board
- https://21x.eu/careers/
- https://fantom.foundation/careers
- https://careers.smartrecruiters.com/Bitoasis
- https://www.coincover.com/careers
- https://careers.koinly.io/jobs
- https://voltz.notion.site/Voltz-Labs-is-Hiring-f1a8857cb7b24d43968cfd735f52292a
- https://careers.bitrefill.com/jobs/
- https://bankless.pallet.com/jobs
- https://www.certora.com/#careers
- https://istari.vision/en/career/
- https://gamescoin.jobs.personio.de/
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
- https://bwarelabs.mingle.ro/en/apply
- https://github.com/tvl-labs/job-board/blob/main/engineering/protocol_engineer.md
- https://wellfound.com/company/redstonefinance/jobs
- https://stake-capital-group.breezy.hr/
- https://polygon.technology/ecosystem-jobs
- https://jobs.dragonfly.xyz/jobs 
- https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/
- https://www.ethswarm.org/jobs
- https://cash.app/careers
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
- https://apply.workable.com/summerfi/#jobs https://summer.fi/
- https://cryptotaxcalculator.io/us/jobs/
- https://careers.transak.com/
- https://transak-inc.breezy.hr
- https://lavanet.applytojob.com/apply/
- https://www.kamu.dev/jobs/
- https://jobs.zama.ai/departments/tfhe-rs
- https://www.soliduslabs.com/careers#open-positions
- https://www.ambergroup.io/people?location=All&jobType=All
- https://lightcurve.jobs.personio.de/?language=en
- https://apply.workable.com/anza-xyz/
