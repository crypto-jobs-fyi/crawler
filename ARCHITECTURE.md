# Crawler architecture

## Overview

The crawler collects job listings from crypto, AI, fintech, and technology
companies. Each crawler entry point selects a company list and delegates the
work to the shared Playwright runner. Scrapers return normalized dictionaries
with `company`, `title`, `location`, and `link` fields.

```text
crawler_*.py / crypto_crawler*.py
              |
              v
  PlaywrightCrawlerRunner
  - browser/context lifecycle
  - headless or headed Chromium
  - retries and structured logging
  - output file locking
              |
              v
       CompanyItem list
              |
              v
       Scrapers registry
              |
              v
       ScrapeIt implementations
       - ATS-specific selectors
       - dynamic content waits
       - consent, pagination, and frames
              |
              v
       JSON job snapshots
```

## Runtime components

### Entry points

Root-level `crawler_*.py` and `crypto_crawler*.py` files configure:

- the company category or ATS subset;
- output and current-count JSON files;
- whether Chromium runs headless;
- any scraper-specific overrides.

The normal crawlers use headless Chromium. The headed entry points are useful
for sites that require a visible browser session, and for local debugging.
New scrapers must remain compatible with the normal headless crawlers and must
not introduce a headed-only requirement.

### `PlaywrightCrawlerRunner`

[`src/playwright_crawler_runner.py`](./src/playwright_crawler_runner.py)
owns the Playwright lifecycle:

1. launch one Chromium browser;
2. create a fresh browser context and page per company attempt;
3. wrap the page in [`PlaywrightPageAdapter`](./src/playwright_adapter.py);
4. invoke the selected `ScrapeIt.getJobs` implementation;
5. retry empty or failed scrapes up to `max_attempts`;
6. close the context and browser;
7. write successful results and current job counts.

The adapter keeps the scraper contract small while providing the locator,
attribute, script, frame, click, and wait operations used by the existing
scrapers. New scrapers may use the adapter for consistency or use native
Playwright APIs when they need functionality not represented by the adapter.

Headless mode filters out companies whose `headless` setting is false.
Huspy is currently marked headless in `companies.json`, but its provider may
return an anti-bot page in headless Chromium; use the headed fintech entry
point when a live run requires it.

### Scraper interface and registry

All scraper classes inherit from [`ScrapeIt`](./src/scrape_it.py) and
implement:

```python
def getJobs(self, page, web_page, company) -> list:
    ...
```

[`src/scrapers.py`](./src/scrapers.py) is the registry used by company
definitions. [`CompanyItem`](./src/company_item.py) stores the company name,
jobs URL, scraper class, company URL, and headless preference.

Every returned job has this shape:

```python
{
    "company": "company-name",
    "title": "Job title",
    "location": "Remote - USA",
    "link": "https://example.com/jobs/123",
}
```

### Data persistence

The base class writes the complete job snapshot and per-company current counts
as JSON. The runner serializes file writes with a lock so future parallel
execution can safely share output files.

## Testing

Tests use `pytest-playwright` and the shared `page` fixture. The contract tests
in [`test/test_playwright_headed_scrapers.py`](./test/test_playwright_headed_scrapers.py)
serve deterministic HTML through Playwright routes and verify scraper output,
including delayed rendering and Coinbase location parsing.

The older company-specific tests are retained as opt-in live smoke tests. They
use the adapter-backed `page_adapter` fixture and are skipped by default because
external job pages can change or block automated traffic:

```bash
pytest
pytest --run-live
pytest test/test_playwright_headed_scrapers.py
```

Install the browser used by the test fixture before running tests:

```bash
python -m playwright install chromium
```

## Workflows

GitHub Actions installs Python dependencies and Chromium before running tests
or crawlers. Crawler workflows validate generated JSON and publish changes
through automated pull requests. Headed workflows run Chromium under Xvfb on
Linux; normal test and headless crawler jobs do not need a virtual display.

The reusable workflow accepts a space-separated list of crawler scripts and
the output file to publish. This keeps category-specific workflows small while
sharing dependency installation, execution, validation, and PR creation.

## Adding a scraper

1. Add `src/scrape_<name>.py`.
2. Inherit from `ScrapeIt`.
3. Implement `getJobs` using Playwright adapter locators or native Playwright.
4. Return the normalized four-field job dictionary.
5. Register the class in `src/scrapers.py`.
6. Add `test/test_<name>_scraper.py` with the pytest-playwright `page` fixture.
   Live scraper tests must navigate to the real target page rather than mock
   network responses.
7. Run the dedicated live test directly, for example
   `pytest --run-live test/test_dayforce_scraper.py`.
8. Add an opt-in live smoke test when useful.

Prefer stable attributes and explicit waits for dynamic content. Keep
site-specific work in its scraper and keep browser lifecycle concerns in the
runner.
