# Crypto Jobs Crawler - Architecture & Analysis

## 1. PROJECT OVERVIEW

**Purpose**: Web scraping system for crypto/fintech job listings from multiple ATS platforms (Ashby, Greenhouse, Lever, etc.)

**Scale**: 
- 39 scraper modules
- 177+ companies tracked
- Multiple vertical-specific crawlers (AI, crypto, fintech, tech)
- Parallel processing with threading
- GitHub Actions CI/CD integration

---

## 2. ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                      ENTRY POINTS (crawler_*.py)                │
│  crawler_ai.py │ crawler_crypto.py │ crawler_tech.py │ crawler_fin.py
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ CrawlerRunner   │
                    │ (Orchestration) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼─────┐    ┌────────▼────────┐   ┌──────▼──────┐
   │Threading │    │ WebDriver Mgmt  │   │Job Processing
   │Queue-based│   │(Chrome headless)│   │(Retries/Lock)
   └────┬─────┘    └────────┬────────┘   └──────┬──────┘
        │                   │                    │
        └───────┬───────────┴────────────────────┘
                │
       ┌────────▼─────────┐
       │  CompanyItem List │
       │ (176 companies)   │
       └────────┬──────────┘
                │
        ┌───────▼──────────────────────────────┐
        │        SCRAPER REGISTRY              │
        │      (Scrapers enum class)           │
        │  45+ scraper implementations:        │
        │  - ScrapeAshbyhq                     │
        │  - ScrapeGreenhouse                  │
        │  - ScrapeLever                       │
        │  - ScrapePaxos, ScrapeCircle, etc.  │
        └───────┬──────────────────────────────┘
                │
        ┌───────▼──────────────────┐
        │  Dynamic Scraper Loading  │
        │ company.scraper_type()    │
        │ Returns ScrapeIt instance │
        └───────┬──────────────────┘
                │
        ┌───────▼──────────────────────────────┐
        │    Individual Scrapers (ScrapeIt)    │
        │  Abstract base with getJobs()        │
        │  - Parse HTML/JS job pages           │
        │  - Extract: title, link, location    │
        │  - Handle dynamic content (Selenium) │
        └───────┬──────────────────────────────┘
                │
       ┌────────▼──────────────────┐
       │   Job Data Processing     │
       │  write_jobs()             │
       │  write_current_jobs_num() │
       │  (JSON file updates)      │
       └────────┬──────────────────┘
                │
       ┌────────▼──────────────────┐
       │   Post-Processing         │
       │  AgeProcessor             │
       │  - Track job appearance   │
       │  - Historical analysis    │
       │  - Aggregate statistics   │
       └────────┬──────────────────┘
                │
       ┌────────▼──────────────────┐
       │   Output Files (JSON)     │
       │  - crypto_jobs.json       │
       │  - crypto_current.json    │
       │  - crypto_jobs_age.json   │
       │  - crypto_history.json    │
       └───────────────────────────┘
```

---

## 3. COMPONENT BREAKDOWN

### 3.1 Entry Points (`crawler_*.py`)
**Files**: 
- Main: `crawler_ai.py`, `crawler_crypto.py`, `crawler_tech.py`, `crawler_fin.py`
- ATS-Specific: `crawler_ai_ashby.py`, `crawler_ai_greenhouse.py`, `crawler_ai_lever.py`
- Crypto alternatives: `crypto_crawler.py`, `crypto_crawler_ashby.py`, etc.
- Headed: `crawler_ai_headed.py`, `crawler_headed.py`, `crawler_fintech_headed.py`

**Responsibility**:
- Load company metadata from `companies.json` via the `Companies` utility class.
- Filter companies by `category` (e.g., "ai", "crypto", "fintech").
- Initialize CrawlerRunner with vertical-specific output files.
- Trigger scraping pipeline.
- For split crawlers: Generate targeted JSON outputs (e.g., `ai_jobs_ashby.json`) to be merged later.

**Characteristics**:
- Lightweight orchestration.
- Uses `Companies.filter_companies(category="...")` for dynamic selection.
- Single responsibility: vertical-specific delegation.

---

### 3.2 CrawlerRunner (Orchestration)
**File**: `src/crawler_runner.py`

**Key Responsibilities**:
1. **Threading Management**
   - Queue-based parallel processing.
   - Default 2 workers for headless mode.
   - Automatically skips `thread` ID in structured logs for cleaner output.

2. **WebDriver Lifecycle**
   - Chrome options: `--no-sandbox`, `--disable-dev-shm-usage`, `--headless`, `--disable-extensions`.
   - Per-worker driver instances.
   - Proper cleanup in finally blocks.

3. **Headless Compatibility**
   - Automatically skips companies with `headless: false` if the runner is in headless mode.
   - Prevents execution of scrapers requiring a head in environments where only headless is supported (e.g., CI/CD).

4. **Retry Logic**
   - 2 retries on 0 jobs returned.
   - 2 seconds delay between retries.
   - Exception handling with structured logging.

5. **Data Persistence**
   - Thread-safe file locking with `threading.Lock()`.
   - Call `ScrapeIt.write_jobs()` and `write_current_jobs_number()`.
   - Metrics: job count, duration, and status codes.

**Methods**:
- `run()` - Main entry point.
- `_worker()` - Thread worker function.
- `_scrape_company()` - Single company orchestration.
- `_get_driver()` - ChromeDriver factory.
- `_initialize_files()` - JSON file setup.

---

### 3.3 Scrapers Registry (`src/scrapers.py`)
**Purpose**: Centralized enum-like registry of all scrapers.

**Current Implementation**:
```python
class Scrapers:
    ROBINHOOD = ScrapeRobinhood
    ASHBYHQ = ScrapeAshbyhq
    LEVER = ScrapeLever
    GREENHOUSE = ScrapeGreenhouse
    # ... 40+ more
```

**Design Pattern**: Factory pattern via class attributes.
- Each attribute = scraper class reference.
- Dynamic instantiation: `company.scraper_type()`.

**Scale**: 45+ scraper implementations.

---

### 3.4 Company Configuration (`companies.json`)
**File**: `companies.json` (Replaces legacy `src/company_*_list.py` files)

**Structure**:
```json
{
  "companies": [
    {
      "name": "kraken",
      "jobs_url": "https://jobs.ashbyhq.com/kraken.com",
      "scraper": "ASHBYHQ",
      "company_url": "https://kraken.com",
      "category": "crypto",
      "enabled": true,
      "headless": true
    }
  ]
}
```

**Characteristics**:
- Centralized JSON registry for 300+ companies.
- `CompanyItem` dataclass supports new fields: `category`, `enabled`, and `headless`.
- Migrated from hard-coded Python lists to externalized configuration.
- Supports runtime enabling/disabling of scrapers without code changes.

---

### 3.5 Companies Utility (`src/companies.py`)
**Purpose**: Data access layer for company configuration.

**Key Features**:
- `load_companies()`: Loads and caches data from `companies.json`.
- `filter_companies(category)`: Returns enabled companies for a specific vertical.
- `get_company(name)`: Retrieves a single company item by name.

---

### 3.6 Scraper Base Class (`src/scrape_it.py`)
**Abstract Interface**:
```python
from src.logging_utils import get_logger

class ScrapeIt(ABC):
    def __init__(self) -> None:
        self.logger = get_logger(f"scraper.{self.__class__.__name__}")

    @abstractmethod
    def getJobs(self, driver, web_page, company) -> list[dict]:
        """Returns [{"company": str, "title": str, "link": str, "location": str}]"""
    
    @staticmethod
    def write_jobs(jobs, filename):
        """Append jobs to JSON file"""
    
    @staticmethod
    def write_current_jobs_number(company, count, filename):
        """Update current job count per company"""
```

**Return Contract**:
```python
{
    "company": "CompanyName",
    "title": "Job Title",
    "link": "https://job-link",
    "location": "City, Country"
}
```

**Logging Helpers**:
- `self.logger.info(...)` uses structured JSON format.
- `src/logging_utils.py` handles field filtering (removes `taskName: null`, skips `thread`).

---

### 3.7 Individual Scrapers
**39 Implementations**: `src/scrape_*.py`

**Examples**:
- `scrape_ashbyhq.py` - Ashby ATS.
- `scrape_lever.py` - Lever ATS.
- `scrape_greenhouse.py` - Greenhouse ATS.
- `scrape_circle.py` - Custom job board.
- `scrape_coinbase.py` - Custom site.

**Common Patterns**:
- Selenium for dynamic content.
- CSS selectors for element extraction.
- Explicit waits for page loads.
- Some need `time.sleep()` for JS rendering.

---

### 3.8 Post-Processing (`src/age_processor.py`)
**Function**: `update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)`

**Pipeline**:
1. Load all jobs from `crypto_jobs.json`.
2. Track new vs existing via link deduplication.
3. Record first appearance date.
4. Compute age: `current_date - first_appearance_date`.
5. Generate per-company statistics.
6. Append to history.

**Outputs**:
- `crypto_current.json` - Current job count by company.
- `crypto_jobs_age.json` - Job age tracking.
- `crypto_history.json` - Historical snapshots.

---

### 3.9 Logging Utilities (`src/logging_utils.py`)
**Purpose**: Centralised structured logging (JSON lines).

**Key Points**:
- **JSON Formatter**: Outputs logs as single-line JSON objects.
- **Field Filtering**: 
  - Automatically omits `thread` ID.
  - Skips keys with `null` values (e.g., `taskName`).
  - Standardizes keys: `timestamp`, `level`, `logger`, `message`, `module`, `function`, `line`.
- **Configuration**: Level control via `CRAWLER_LOG_LEVEL`.
- **Integration**: All scrapers and runner components use `get_logger()`.

### 3.10 Merging Utilities (`merge_*_jobs.py`)
**Files**: `merge_ai_jobs.py`, `merge_crypto_jobs.py`, `merge_fintech_jobs.py`

**Purpose**: Aggregates job listings from multiple ATS-specific or headed/headless crawl results into a single unified JSON file per vertical.

**Key Features**:
- **De-duplication**: Uses link-based `seen` sets to ensure unique entries.
- **Unified Schema**: Standardizes output format for downstream processing.
- **Vertical-Specific**: Each script handles its own set of source files (e.g., `crypto_jobs_lever.json` → `crypto_jobs.json`).

---

## 4. DATA FLOW

```
Input: companies.json (300+ items)
   ↓
[Companies Utility]
   ├─ Load from JSON
   └─ Filter by category (AI, Crypto, Tech, Fintech)
   ↓
[CrawlerRunner]
   ├─ Filter out headed-only companies (if run in headless mode)
   ├─ Queue companies
   ├─ Spawn N worker threads
   │  ├─ Get WebDriver
   │  └─ For each company:
   │      ├─ Load scraper class
   │      ├─ Call getJobs()
   │      ├─ Retry logic (max 2)
   │      ├─ Thread-safe write to crypto_jobs.json
   │      └─ Update crypto_current.json
   └─ Join threads, close drivers
   ↓
[AgeProcessor]
   ├─ Deduplicate jobs by link
   ├─ Calculate age (days old)
   ├─ Aggregate statistics
   └─ Save history
   ↓
Output Files:
   ├─ crypto_jobs.json (all jobs)
   ├─ crypto_current.json (per-company count)
   ├─ crypto_jobs_age.json (age tracking)
   └─ crypto_history.json (trends)
```

---

## 5. CURRENT STRENGTHS

✅ **Modular Design**
- Clear separation: orchestration ↔ scraping ↔ processing
- Abstract base class for extensibility
- Easy to add new scrapers

✅ **Parallel Processing**
- Threading for headless mode
- Efficient resource utilization
- Configurable worker count

✅ **Robust Error Handling**
- Retry logic with exponential backoff-like delays
- Per-company exception isolation
- Graceful degradation

✅ **Multi-Vertical Support**
- Separate crawlers for AI, crypto, fintech, tech.
- Reusable company lists and filters via `Companies` utility.
- Shared scraper infrastructure.

✅ **Centralized Configuration**
- `companies.json` allows updates without code changes.
- Metadata-driven (category, enabled, headless).

✅ **Structured Logging**
- JSON-based logs for all components.
- Automatic removal of verbose fields (thread, null taskName).

✅ **Data Integrity**
- Thread-safe JSON writes with locks.
- Deduplication via link tracking.
- Historical trending.

---

## 6. IDENTIFIED ISSUES & BOTTLENECKS

### 6.1 Configuration Management (Recently Improved)
- **Status**: ✅ Transitioned from Python-based lists to `companies.json`.
- **Remaining**: Needs easier GUI or tool for non-dev updates.

### 6.2 Scraper Maintenance
**Problem**: 39 scrapers with varying quality/reliability
- Some require `time.sleep()` hacks instead of proper waits
- No standardized error handling across scrapers
- Cookie banners/CAPTCHAs break some scrapers (Coinbase, Gemini)
- Manual fixes needed when site structure changes

**Impact**: High maintenance burden, frequent failures

### 6.3 Retry Strategy
**Problem**: Fixed 2 retries with 2-second delay
- Not adaptive to failure type (timeout vs parse error)
- No exponential backoff
- No dead-letter queue for persistent failures

**Impact**: Wasted time on unrecoverable failures, slow recovery

### 6.4 Logging & Observability (Recently Improved)
- **Status**: ✅ Implemented structured JSON logging.
- **Remaining**: Needs log aggregation (e.g., Loki) and dashboards.

### 6.5 Testing Coverage
**Problem**: Recently refactored tests but still gaps
- Some tests fail due to company having 0 positions (Bitfinex)
- No mock Selenium tests (all require real browser)
- Cookie banner tests failing (Coinbase, Gemini)

**Impact**: Flaky test suite, slow CI/CD

### 6.6 Data Deduplication
**Problem**: Link-based deduplication only
- No handling of job URL changes (same job, different URL)
- No semantic deduplication (same position reposted)
- Duplicate counting in `write_current_jobs_number()`

**Impact**: Inflated job counts, inaccurate analytics

### 6.7 Driver Lifecycle
**Problem**: One driver per worker thread
- Not optimal for scraping (high memory/startup overhead)
- No connection pooling for efficiency
- No screenshot capture on failure for debugging

**Impact**: Resource-heavy, hard to troubleshoot

### 6.8 Rate Limiting
**Problem**: No rate limiting or delays between requests
- Risk of IP blocking
- No respect for site ToS
- No backpressure mechanism

**Impact**: Potential blacklisting

---

## 7. IMPROVEMENT PLAN

### PHASE 1: IMMEDIATE (Quick Wins)
**Effort**: 1-2 weeks

#### 1.1 Structured Logging (✅ COMPLETED)
- Distributed JSON logging implemented.
- Field filtering for `thread` and `taskName` added.

#### 1.2 Explicit Waits Everywhere
```python
# Replace time.sleep() with proper WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, timeout=10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "job-item")))
```

**Benefits**:
- Faster execution (waits only as long as needed)
- More reliable (handles varied load times)
- Standard Selenium pattern

#### 1.3 Adaptive Retry Logic
```python
class RetryPolicy:
    MAX_RETRIES = {
        "TIMEOUT": 3,
        "PARSE_ERROR": 1,
        "ZERO_JOBS": 2,
        "CAPTCHA": 0
    }
    
    BACKOFF = {
        1: 1,    # 1 second
        2: 5,    # 5 seconds
        3: 30    # 30 seconds
    }

# Usage:
for attempt, error_type in enumerate(failures):
    if attempt > RetryPolicy.MAX_RETRIES.get(error_type, 1):
        logger.warn(f"Giving up on {error_type}")
        break
    delay = RetryPolicy.BACKOFF.get(attempt + 1, 60)
    time.sleep(delay)
```

**Benefits**:
- Smarter retry decisions
- Exponential backoff reduces server load
- Faster failure detection

---

### PHASE 2: CONFIGURATION (✅ COMPLETED)

#### 2.1 JSON Configuration File
- Migrated all company lists to `companies.json`.
- Implemented `Companies` utility for filtering and loading.

#### 2.2 Scraper Configuration (In progress)
**Goal**: Move CSS selectors and timeouts into JSON config.

---

### PHASE 3: RELIABILITY (2-3 weeks)

#### 3.1 Dead-Letter Queue
```python
class CrawlerRunner:
    def __init__(self, ...):
        self.dead_letter_queue = []  # Failed companies
    
    def _log_failure(self, company, error, traceback):
        self.dead_letter_queue.append({
            "company": company.name,
            "error": str(error),
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback
        })
    
    def save_failures(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.dead_letter_queue, f, indent=2)
```

**Usage**:
```python
runner = CrawlerRunner(...)
runner.run(companies)
runner.save_failures("failures.json")

# CI/CD: Fail if too many failures
if len(runner.dead_letter_queue) > MAX_ALLOWED:
    sys.exit(1)
```

**Benefits**:
- Visibility into persistent failures
- Replay mechanism
- Failure analysis

#### 3.2 Health Checks
```python
class HealthCheck:
    @staticmethod
    def validate_output(jobs_file, current_file):
        """Post-scrape validation"""
        with open(jobs_file) as f:
            jobs = json.load(f).get('data', [])
        
        # Check: reasonable job count
        if len(jobs) < 100:
            logger.error(f"Suspiciously low job count: {len(jobs)}")
            return False
        
        # Check: no duplicates
        links = [j['link'] for j in jobs]
        if len(links) != len(set(links)):
            logger.error(f"Duplicate jobs detected: {len(links) - len(set(links))}")
            return False
        
        return True

# In crawler runner:
if not HealthCheck.validate_output(jobs_file, current_file):
    logger.error("Health check failed, aborting")
    sys.exit(1)
```

**Benefits**:
- Early detection of systemic failures
- Prevents corrupted data publication
- Actionable alerts

#### 3.3 Proxy/Rate Limiting
```python
from urllib.request import ProxyHandler

def get_driver_with_proxy(proxy_list):
    chrome_options = webdriver.ChromeOptions()
    proxy = random.choice(proxy_list)
    chrome_options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=chrome_options)

class RateLimiter:
    def __init__(self, delay_between_requests=0.5):
        self.delay = delay_between_requests
        self.last_request = 0
    
    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request = time.time()
```

**Benefits**:
- Avoid IP blocking
- Respectful scraping
- Reduced risk of legal issues

---

### PHASE 4: SCALABILITY (3-4 weeks)

#### 4.1 Database Backend
```python
# Replace JSON files with SQLite/PostgreSQL
from sqlalchemy import Column, String, DateTime, Integer

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    company = Column(String, index=True)
    title = Column(String)
    link = Column(String, unique=True)
    location = Column(String)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

# Benefits: ACID compliance, indexing, querying, transactions
```

#### 4.2 API Layer
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/jobs")
async def get_jobs(company: str = None, days_old: int = None):
    query = db.session.query(Job)
    if company:
        query = query.filter_by(company=company)
    if days_old:
        cutoff = datetime.utcnow() - timedelta(days=days_old)
        query = query.filter(Job.first_seen >= cutoff)
    return query.all()

@app.get("/stats")
async def get_stats():
    return {
        "total_jobs": db.session.query(Job).count(),
        "companies": db.session.query(Job.company).distinct().count(),
        "by_company": [...]
    }
```

**Benefits**:
- Queryable interface
- Real-time data access
- Supports dashboards/clients

#### 4.3 Distributed Scraping
```python
# Use Celery for distributed workers
from celery import Celery

app = Celery('crawler')

@app.task(bind=True, max_retries=3)
def scrape_company(self, company_id):
    try:
        company = load_company(company_id)
        jobs = scrape_company_safe(company)
        save_jobs(company, jobs)
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

# Scale horizontally: N workers, unlimited companies
```

**Benefits**:
- Handle 1000s of companies
- Fault tolerance
- Load balancing

---

## 8. TESTING STRATEGY

### Current State
- ✅ 22+ refactored pytest tests
- ⚠️ Some failing (0 jobs, cookie banners, timeouts)

### Proposed Strategy

```python
# tests/integration/test_scraper_ashbyhq_live.py
@pytest.mark.integration
@pytest.mark.slow
def test_ashbyhq_live():
    """Real browser test - runs only in CI nightly"""
    scraper = ScrapeAshbyhq()
    driver = webdriver.Chrome()
    try:
        jobs = scraper.getJobs(driver, "https://jobs.ashbyhq.com/kraken", "Kraken")
        assert len(jobs) > 0
    finally:
        driver.quit()

# Parameterized tests for all scrapers
@pytest.mark.parametrize("scraper_class,company_name,url", [
    (ScrapeAshbyhq, "kraken", "https://jobs.ashbyhq.com/kraken"),
    (ScrapeLever, "binance", "https://jobs.lever.co/binance"),
])
def test_scraper_integration(scraper_class, company_name, url):
    """Integration tests for all scrapers with real browser"""
    scraper = scraper_class()
    driver = webdriver.Chrome()
    try:
        jobs = scraper.getJobs(driver, url, company_name)
        for job in jobs:
            assert "company" in job
            assert "title" in job
            assert "link" in job
            assert "location" in job
    finally:
        driver.quit()
```

**Test Strategy**:
- **Integration Tests (Real Browser)**: 80% - smoke tests on real sites
- **E2E Tests (Full Pipeline)**: 20% - full crawl on schedule

---

## 9. IMPLEMENTATION ROADMAP

```
PHASE 1: Quick Wins (Weeks 1-2)
├─ Structured logging (all components)
├─ Explicit waits (all scrapers)
└─ Adaptive retries (CrawlerRunner)

PHASE 2: Configuration (Weeks 3-4)
├─ YAML company config
├─ Scraper selector config
└─ Runtime loading + filtering

PHASE 3: Reliability (Weeks 5-7)
├─ Dead-letter queue
├─ Health checks
├─ Rate limiting + proxy support
└─ Cookie banner handling (specific scrapers)

PHASE 4: Scalability (Weeks 8-11)
├─ Database backend (SQLite → Postgres)
├─ REST API layer (FastAPI)
├─ Celery distributed workers
└─ Monitoring/alerting (Prometheus + Grafana)
```

---

## 10. SUCCESS METRICS

| Metric | Current | Target (6 months) |
|--------|---------|-------------------|
| Job Count Accuracy | 95% | 99%+ |
| Scraper Success Rate | 85% | 95%+ |
| Test Coverage | 40% | 80%+ |
| Median Scrape Time | 45min (2 workers) | 15min (parallel) |
| Time to Add New Scraper | 30min code + deploy | 5min config |
| Mean Time to Fix Failed Scraper | 2 hours (manual) | 15min (logs + replay) |
| Data Freshness | 2x/week | Daily |
| Observability | Print logs | Structured logs + dashboards |

---

## 11. DEPENDENCIES & TOOLING

### Current
- `selenium==4.34.2` - WebDriver
- `pytest==9.0.2` - Testing
- `urllib3==2.5.0` - HTTP
- `jsonschema==4.25.0` - Validation

### Recommended Additions
- `sqlalchemy` - ORM
- `fastapi` - API
- `celery` - Distributed tasks
- `redis` - Task broker
- `python-logging-loki` - Log aggregation
- `prometheus-client` - Metrics
- `pytest-xdist` - Parallel tests
- `beautifulsoup4` - HTML parsing (alternative to Selenium for static pages)

---

## 12. CONCLUSION

The crawler has **strong fundamentals** (modular, threaded, extensible) but needs **operational improvements** (logging, configuration, testing). The roadmap prioritizes **quick wins** first (logging, retries) before **architectural changes** (database, API). Estimated effort: **3-4 months** for full implementation.

**Immediate Action Items**:
1. Replace `time.sleep()` with explicit waits in all scrapers.
2. Implement Dead-Letter Queue for failed companies.
3. Improve test coverage for cookie banner handling.
4. Scale workers (max_workers) for faster completion.
