# GitHub Copilot Instructions for crypto-jobs-crawler

This repository is a Python-based web crawler designed to scrape job listings from various crypto and AI company websites and ATS (Applicant Tracking Systems) like Ashby, Greenhouse, and Lever.

## Architecture & Core Components

- **Orchestration**: The entry points are `crawler_*.py` files (e.g., `crawler_ai.py`, `crawler_tech.py`). These scripts initialize the Selenium WebDriver, iterate through company lists, and invoke the appropriate scrapers.
- **Scraper Interface**: All scrapers must inherit from the `ScrapeIt` abstract base class defined in `src/scrape_it.py`.
  - **Required Method**: `getJobs(self, driver, web_page, company) -> list`
  - **Output**: Returns a list of dictionaries, each containing `company`, `title`, `location`, and `link`.
- **Data Models**:
  - `CompanyItem` (`src/company_item.py`): A dataclass defining a target company, its jobs URL, and the scraper class to use.
- **Company Lists**: Defined in `src/company_*_list.py` (e.g., `src/company_ai_list.py`). These functions return a list of `CompanyItem` objects.
- **Data Storage**: Results are written to JSON files (e.g., `ai_jobs.json`, `ai_current_jobs.json`) using static methods in `ScrapeIt`.

## Development Workflow

### Environment Setup
1.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running Crawlers
Run a specific crawler script from the root directory:
```bash
python crawler_ai.py
```
*Note: The crawlers run in headless mode by default. To debug visually, comment out `chrome_options.add_argument('--headless')` in the crawler script.*

### Testing
Tests are located in the `test/` directory and use `pytest`.
- Run all tests:
  ```bash
  pytest
  ```
- Run a specific test file:
  ```bash
  pytest test/test_greenhouse_scraper.py
  ```

## Coding Conventions

### Creating a New Scraper
1.  Create a new file `src/scrape_<name>.py`.
2.  Define a class inheriting from `ScrapeIt`.
3.  Implement the `getJobs` method.
4.  Use Selenium `driver` to navigate and extract data.
5.  **Example Pattern**:
    ```python
    from src.scrape_it import ScrapeIt
    from selenium.webdriver.common.by import By

    class ScrapeMyATS(ScrapeIt):
        name = 'MY_ATS'

        def getJobs(self, driver, web_page, company) -> list:
            driver.get(web_page)
            # ... scraping logic ...
            return result # list of dicts
    ```

### Adding a Company
1.  Import the scraper class in the appropriate list file (e.g., `src/company_ai_list.py`).
2.  Add a `CompanyItem` to the list:
    ```python
    CompanyItem('CompanyName', 'https://jobs.url', ScrapeMyATS, 'https://company.url')
    ```

### Error Handling
- Scrapers should be robust. If a specific company fails, the main loop in `crawler_*.py` catches the exception and continues to the next company.
- Use `driver.implicitly_wait` or explicit waits to handle dynamic content loading.

### Dependencies
- **Selenium**: Used for all browser automation.
- **Docker**: A `Dockerfile` is provided for containerized execution.
