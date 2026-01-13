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
       │  - jobs.json              │
       │  - current.json           │
       │  - jobs_age.json          │
       │  - history.json           │
       └───────────────────────────┘
```

---

## 3. COMPONENT BREAKDOWN

### 3.1 Entry Points (`crawler_*.py`)
**Files**: `crawler_ai.py`, `crawler_crypto.py`, `crawler_tech.py`, `crawler_fin.py`

**Responsibility**:
- Load company lists by vertical
- Filter companies (e.g., exclude Ashby/Greenhouse/Lever)
- Initialize CrawlerRunner
- Trigger scraping pipeline

**Characteristics**:
- Lightweight orchestration
- ~15 lines of code each
- Single responsibility: delegation

---

### 3.2 CrawlerRunner (Orchestration)
**File**: `src/crawler_runner.py`

**Key Responsibilities**:
1. **Threading Management**
   - Queue-based parallel processing
   - Default 2 workers for headless mode
   - Single-threaded fallback for non-headless

2. **WebDriver Lifecycle**
   - Chrome options: `--no-sandbox`, `--disable-dev-shm-usage`, `--headless`, `--disable-extensions`
   - Per-worker driver instances
   - Proper cleanup in finally blocks

3. **Retry Logic**
   - 2 retries on 0 jobs returned
   - 2 seconds delay between retries
   - Exception handling with retry support

4. **Data Persistence**
   - Thread-safe file locking with `threading.Lock()`
   - Call `ScrapeIt.write_jobs()` and `write_current_jobs_number()`
   - Metrics: job count, timestamps

**Methods**:
- `run()` - Main entry point
- `_worker()` - Thread worker function
- `_scrape_company()` - Single company orchestration
- `_get_driver()` - ChromeDriver factory
- `_initialize_files()` - JSON file setup

---

### 3.3 Scrapers Registry (`src/scrapers.py`)
**Purpose**: Centralized enum-like registry of all scrapers

**Current Implementation**:
```python
class Scrapers:
    ROBINHOOD = ScrapeRobinhood
    ASHBYHQ = ScrapeAshbyhq
    LEVER = ScrapeLever
    GREENHOUSE = ScrapeGreenhouse
    # ... 40+ more
```

**Design Pattern**: Factory pattern via class attributes
- Each attribute = scraper class reference
- Dynamic instantiation: `company.scraper_type()`

**Scale**: 45+ scraper implementations

---

### 3.4 Company Configuration (`src/company_*.py`)
**Files**: 
- `company_list.py` (main - 177 companies)
- `company_ai_list.py`, `company_crypto_list.py`, `company_fin_list.py`, `company_tech_list.py`

**Structure**:
```python
CompanyItem(
    company_name="Name",
    jobs_url="https://...",
    scraper_type=Scrapers.ASHBYHQ,  # or similar
    company_url="https://..."
)
```

**Characteristics**:
- Hard-coded list of companies
- Maps company → jobs URL → scraper type
- Supports filtering by scraper type (e.g., exclude Ashby)

---

### 3.5 Scraper Base Class (`src/scrape_it.py`)
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
- `self.log_info(...)`, `self.log_warning(...)`, and `self.log_error(...)` proxy to a structured logger per scraper instance.
- `src/logging_utils.py` centralises configuration (JSON output, level control via `CRAWLER_LOG_LEVEL`).

---

### 3.6 Individual Scrapers
**39 Implementations**: `src/scrape_*.py`

**Examples**:
- `scrape_ashbyhq.py` - Ashby ATS
- `scrape_lever.py` - Lever ATS
- `scrape_greenhouse.py` - Greenhouse ATS
- `scrape_circle.py` - Custom job board
- `scrape_coinbase.py` - Custom site

**Common Patterns**:
- Selenium for dynamic content
- CSS selectors for element extraction
- Explicit waits for page loads
- Some need `time.sleep()` for JS rendering

---

### 3.7 Post-Processing (`src/age_processor.py`)
**Function**: `update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)`

**Pipeline**:
1. Load all jobs from `jobs.json`
2. Track new vs existing via link deduplication
3. Record first appearance date
4. Compute age: `current_date - first_appearance_date`
5. Generate per-company statistics
6. Append to history

**Outputs**:
- `current.json` - Current job count by company
- `jobs_age.json` - Job age tracking
- `history.json` - Historical snapshots

---

### 3.8 Logging Utilities (`src/logging_utils.py`)
**Purpose**: Centralised structured logging (JSON lines) for crawlers, scrapers, and utilities.

**Key Points**:
- `configure_logging()` installs a shared `StreamHandler` with JSON formatter; level overridable via `CRAWLER_LOG_LEVEL`.
- `get_logger(name)` returns cached `logging.Logger` instances scoped per module/class.
- Scrapers and scripts extend `ScrapeIt.log_*` helpers for consistent event metadata (`company`, `attempt`, `duration_seconds`, etc.).
- Outputs are UTF-8 JSON objects, safe for ingestion by log pipelines or GitHub Actions artifacts.

---

## 4. DATA FLOW

```
Input: Company List (177+ items)
   ↓
[CrawlerRunner]
   ├─ Queue companies
   ├─ Spawn N worker threads
   │  ├─ Get WebDriver
   │  └─ For each company:
   │      ├─ Load scraper class
   │      ├─ Call getJobs()
   │      ├─ Retry logic (max 2)
   │      ├─ Thread-safe write to jobs.json
   │      └─ Update current.json
   └─ Join threads, close drivers
   ↓
[AgeProcessor]
   ├─ Deduplicate jobs by link
   ├─ Calculate age (days old)
   ├─ Aggregate statistics
   └─ Save history
   ↓
Output Files:
   ├─ jobs.json (all jobs)
   ├─ current.json (per-company count)
   ├─ jobs_age.json (age tracking)
   └─ history.json (trends)
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
- Separate crawlers for AI, crypto, fintech, tech
- Reusable company lists and filters
- Shared scraper infrastructure

✅ **Data Integrity**
- Thread-safe JSON writes with locks
- Deduplication via link tracking
- Historical trending

---

## 6. IDENTIFIED ISSUES & BOTTLENECKS

### 6.1 Configuration Management
**Problem**: Hard-coded company lists in Python files
- No database; changes require code edits + deployment
- No runtime filtering/exclusion without redefining lists
- Duplicate company data across `company_list.py` and vertical lists

**Impact**: Low operational flexibility, deployment friction

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

### 6.4 Logging & Observability
**Problem**: Print statements only
- No structured logging (JSON, levels)
- No persistent logs for post-analysis
- Difficult to debug failures in CI/CD

**Impact**: Poor visibility into system behavior

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

#### 1.1 Structured Logging
```python
from src.logging_utils import get_logger

logger = get_logger("crawler.runner")
logger.info("Scrape start", extra={"company": company_name, "attempt": attempt})
logger.error(
    "Scrape failed",
    extra={"company": company_name, "attempt": attempt},
    exc_info=True,
)
```

**Benefits**: 
- Persistent logs for debugging
- Structured output for analysis
- Easy integration with monitoring

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

### PHASE 2: CONFIGURATION (1-2 weeks)

#### 2.1 JSON Configuration File
```json
{
  "companies": [
    {
      "name": "kraken",
      "jobs_url": "https://jobs.ashbyhq.com/kraken.com",
      "scraper": "ASHBYHQ",
      "company_url": "https://kraken.com",
      "enabled": true,
      "category": "crypto",
      "retry_policy": "STANDARD"
    },
    {
      "name": "paxos",
      "jobs_url": "https://www.paxos.com/jobs",
      "scraper": "PAXOS",
      "company_url": "https://www.paxos.com",
      "enabled": true,
      "category": "fintech",
      "retry_policy": "AGGRESSIVE"
    }
  ]
}
```

**Load at runtime**:
```python
def load_companies_from_json(filename):
    with open(filename) as f:
        config = json.load(f)
    return [CompanyItem(**c) for c in config['companies']]
```

**Benefits**:
- No code redeploys for config changes
- Easy on/off toggles
- Per-company tuning (retry policies, etc.)

#### 2.2 Scraper Configuration
```json
{
  "scrapers": {
    "ASHBYHQ": {
      "timeout": 10,
      "selectors": {
        "job_container": "div.job-item",
        "title": "h2.job-title",
        "location": "span.location"
      },
      "wait_for": ["div.job-item"]
    },
    "LEVER": {
      "timeout": 8,
      "selectors": {},
      "cookie_banner": "div.cookie-consent"
    }
  }
}
```

**Benefits**:
- Reduced scraper code duplication
- Easy A/B testing selectors
- Centralized maintenance

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
1. Add structured logging everywhere
2. Replace `time.sleep()` with explicit waits
3. Create mock test suite
4. Move companies to YAML config
