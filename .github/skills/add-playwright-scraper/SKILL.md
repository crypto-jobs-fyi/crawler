---
name: add-playwright-scraper
description: "Add a new headless Playwright job scraper, company configuration, live test, and registry wiring."
disable-model-invocation: true
argument-hint: "Company name, jobs URL, scraper details, and any selectors or example job URLs"
---
Add a new Playwright scraper for the requested company and job site.

Requirements:

1. Inspect existing scraper, adapter, registry, company configuration, and test
   patterns before editing. Reuse helpers from
   [`src/playwright_adapter.py`](../../src/playwright_adapter.py) and
   [`src/scrape_it.py`](../../src/scrape_it.py).
2. Create `src/scrape_<provider>.py` with a `ScrapeIt` implementation whose
   `getJobs(page, web_page, company)` returns dictionaries containing exactly
   `company`, `title`, `location`, and `link`.
3. Use stable selectors and Playwright waits for dynamically rendered content.
   Handle consent banners, pagination, duplicate cards, missing fields, and
   absolute job links when the target site requires them.
4. The scraper must work in headless Chromium. Do not add a headed-only
   scraper, headed entry point, or `headless=False` override for the new
   company.
5. Register the scraper in [`src/scrapers.py`](../../src/scrapers.py) and
   update the matching entry in [`companies.json`](../../companies.json) with
   the new scraper name and the correct headless setting.
6. Add
   `test/test_<provider>_scraper.py` using the pytest-playwright `page`
   fixture. The test must navigate to the real target page and must not mock
   network responses with `page.route`, synthetic HTML, or request stubs.
   Gate live-site execution with the repository’s `--run-live` option when
   appropriate.
7. The dedicated test must print the scraped result as JSON, including the
   number of job cards and the full `jobs` array. Verify at least one known
   job’s title, location, and link.
8. Add a top-of-file run comment like:

   ```python
   # Run: pytest -q -s --run-live test/test_<provider>_scraper.py
   ```

9. Update directly related documentation only when the new provider or
   workflow introduces a reusable behavior.
10. Validate with:

    ```bash
    python -m compileall -q src test *.py
    pytest -q -s --run-live test/test_<provider>_scraper.py
    git diff --check
    ```

Report the files changed, the live job-card count, and the validation results.
