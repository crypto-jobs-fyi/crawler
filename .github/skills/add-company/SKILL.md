---
name: add-company
description: "Quickly add one or more companies that use an existing job-board scraper."
disable-model-invocation: true
argument-hint: "Company name, company URL, jobs URL, and category (ai, crypto, fintech, or tech)"
---
Add the requested company or companies to [`companies.json`](../../companies.json)
using the repository's existing scraper configuration.

1. Check `companies.json` for duplicate company names and jobs URLs before
   editing. Preserve the existing entry format and ordering; add each company
   beside entries in its category.
2. Use the provided company name, company URL, jobs URL, and category. If any
   required value is missing or ambiguous, ask rather than inventing it.
3. Identify the job-board provider from the jobs URL and choose the matching
   scraper already registered in [`src/scrapers.py`](../../src/scrapers.py).
   Use the exact enum name as the `scraper` value. Do not create a scraper or
   change application code for this config-only task.
4. Only use categories already present in the config: `ai`, `crypto`, `fintech`,
   or `tech`. Set `enabled` and `headless` to `true` unless the user requests
   otherwise or there is a specific, verified reason not to.
5. If the provider does not have an existing scraper, do not guess or silently
   build one. Explain that the job board is unsupported and point to
   [`add-playwright-scraper.prompt.md`](add-playwright-scraper.prompt.md).
6. Validate the JSON with `python -m json.tool companies.json`, run
   `pytest -q test/test_company_list.py` if pytest is available, and run
   `git diff --check`.
7. Summarize the company entries added, chosen scraper(s), and validation
   results.
