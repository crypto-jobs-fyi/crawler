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
    playwright install chromium
    ```
2.  **Run Crawler**:
    ```bash
    python crawler_ai.py
    ```
    *Note: Crawlers run in headless mode by default. To debug visually, disable headless mode in the crawler script.*

To run only the FinTech companies that use Ashby:

```bash
python crawler_fin_ashby.py
```

To run only the FinTech companies that use Greenhouse:

```bash
python crawler_fin_greenhouse.py
```

All crawlers use Playwright. The headed crypto crawler is useful for sites that
need a visible browser session:

```bash
python crypto_crawler_headed.py
```

It launches visible Chromium and runs the same migrated scraper classes as the
normal crawlers.

For the fintech headed workflow:

```bash
python crawler_fintech_headed.py
```

The fintech entry point uses two attempts per company. It runs Huspy and
Revolut with a visible browser because their providers may challenge headless
Chromium. Revolut is configured with `headless: false` in `companies.json`.

### Docker
- `docker build --tag scrap:latest .`
- `docker run --rm -it -v ${PWD}:/data scrap:latest`

## UI
The scraped data is aggregated into a unified dashboard. You can view the live version on GitHub Pages: [crypto-jobs-fyi.github.io/web/](https://crypto-jobs-fyi.github.io/web/)

### Running UI Locally
To view the dashboard on your local machine:
1.  **Generate Data**: Ensure you have run the crawlers or merge scripts to generate the `.json` files (e.g., `ai_jobs.json`, `crypto_jobs.json`, etc.) in the root directory.
2.  **Start Server**: Run a local HTTP server from the root directory:
    ```bash
    python3 -m http.server 8000
    ```
3.  **View**: Open [http://localhost:8000](http://localhost:8000) in your browser.

The UI will automatically fetch and combine job listings from all available vertical JSON files.

## Testing

Tests are located in the `test/` directory and use `pytest-playwright`.
Deterministic contract tests run by default. Company-specific tests that call
external job sites are opt-in:

```bash
pytest
pytest --run-live
```

Install Chromium once before running tests:

```bash
python -m playwright install chromium
```


## Development

### Adding a New Company
1. Add the company to `companies.json` with its name, company URL, jobs URL,
   scraper, and category (`ai`, `crypto`, `fintech`, or `tech`).
2. Reuse a scraper already registered in `src/scrapers.py` when the company uses
   a supported job-board provider.
3. In Copilot Chat, use the
   [Add company prompt](.github/prompts/add-company.prompt.md) to handle the
   config-only addition. For an unsupported provider that needs a new scraper,
   use the [Add Playwright scraper prompt](.github/prompts/add-playwright-scraper.prompt.md).

### Creating a Custom Scraper
1.  Create `src/scrape_<name>.py` inheriting from `ScrapeIt`.
2.  Implement `getJobs(self, page, web_page, company)`.
3.  Use the Playwright adapter or native Playwright locators.
4.  Ensure it works in headless Chromium; new scrapers must not require a
    headed entry point.
5.  Add `test/test_<name>_scraper.py` with the pytest-playwright `page`
    fixture. Live scraper tests must navigate to the real target page rather
    than mocking network responses. Run them with `--run-live`, for example:
    `pytest --run-live test/test_dayforce_scraper.py`.
6.  Register the new scraper in `src/scrapers.py`.

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
- https://careers.smartrecruiters.com/MicroStrategy1
- https://support.bitmart.com/hc/en-us/categories/10942109789723-Career-Opportunities
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
- https://jobs.lever.co/neednova
- https://plaid.com/careers/openings

to be fixed:

"name": "RadicalAI",
"jobs_url": "https://app.nodi.global/company/Radical%20AI"

"name": "fireblocks",
"jobs_url": "https://www.fireblocks.com/careers#open-roles"
