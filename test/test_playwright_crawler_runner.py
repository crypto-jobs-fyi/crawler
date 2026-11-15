import json
import threading
from urllib.parse import quote

import pytest

import src.playwright_crawler_runner as runner_module
from src.company_item import CompanyItem
from src.playwright_adapter import By
from src.playwright_crawler_runner import PlaywrightCrawlerRunner
from src.scrape_it import ScrapeIt


@pytest.fixture
def fake_playwright(monkeypatch):
    browsers = []

    class FakeContext:
        def __init__(self):
            self.thread_id = threading.get_ident()

        def new_page(self):
            assert threading.get_ident() == self.thread_id
            return object()

        def close(self):
            assert threading.get_ident() == self.thread_id

    class FakeBrowser:
        def __init__(self):
            self.thread_id = threading.get_ident()
            self.closed = False
            browsers.append(self)

        def new_context(self):
            assert threading.get_ident() == self.thread_id
            return FakeContext()

        def close(self):
            assert threading.get_ident() == self.thread_id
            self.closed = True

    class FakePlaywright:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    monkeypatch.setattr(runner_module, "sync_playwright", FakePlaywright)
    monkeypatch.setattr(PlaywrightCrawlerRunner, "_launch_browser", lambda self, playwright: FakeBrowser())
    return browsers


def company(name, scraper, *, headless=True, jobs_url="https://example.com/jobs"):
    return CompanyItem(name, jobs_url, scraper, "https://example.com", headless=headless)


def job(name):
    return {
        "company": name,
        "title": f"Job at {name}",
        "location": "Remote",
        "link": f"https://example.com/{name}",
    }


@pytest.mark.parametrize("workers", [0, -1, 1.5, True])
def test_invalid_worker_count_does_not_initialize_files(tmp_path, workers):
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text("existing")

    with pytest.raises(ValueError, match="max_workers must be a positive integer"):
        PlaywrightCrawlerRunner(str(jobs_file), str(tmp_path / "current.json"), max_workers=workers)

    assert jobs_file.read_text() == "existing"


def test_parallel_workers_overlap_and_write_in_company_order(tmp_path, fake_playwright):
    lock = threading.Lock()
    second_finished = threading.Event()
    active = 0
    max_active = 0
    completed = []

    class ControlledScraper(ScrapeIt):
        def getJobs(self, page, web_page, company):
            nonlocal active, max_active
            with lock:
                active += 1
                max_active = max(max_active, active)
            try:
                if company == "first":
                    assert second_finished.wait(timeout=10), "second company did not run concurrently"
                with lock:
                    completed.append(company)
                if company == "second":
                    second_finished.set()
                return [job(company)]
            finally:
                with lock:
                    active -= 1

    names = ["first", "second", "third", "fourth"]
    jobs_file = tmp_path / "jobs.json"
    current_file = tmp_path / "current.json"
    runner = PlaywrightCrawlerRunner(str(jobs_file), str(current_file), max_workers=2, max_attempts=1)
    runner.run([company(name, ControlledScraper) for name in names])

    assert max_active == 2
    assert completed.index("second") < completed.index("first")
    assert [item["company"] for item in json.loads(jobs_file.read_text())["data"]] == names
    assert json.loads(current_file.read_text()) == {**dict.fromkeys(names, 1), "total_jobs": 4}
    assert len(fake_playwright) == 2
    assert len({browser.thread_id for browser in fake_playwright}) == 2
    assert all(browser.closed for browser in fake_playwright)


def test_parallel_retries_and_empty_results(tmp_path, fake_playwright, monkeypatch):
    monkeypatch.setattr(runner_module.time, "sleep", lambda seconds: None)
    attempts = {}

    class RetryScraper(ScrapeIt):
        def getJobs(self, page, web_page, company):
            attempts[company] = attempts.get(company, 0) + 1
            if company == "empty":
                return []
            if attempts[company] == 1:
                raise RuntimeError("temporary failure")
            return [job(company)]

    jobs_file = tmp_path / "jobs.json"
    current_file = tmp_path / "current.json"
    runner = PlaywrightCrawlerRunner(str(jobs_file), str(current_file), max_workers=2, max_attempts=2)
    runner.run([company("retry", RetryScraper), company("empty", RetryScraper)])

    assert attempts == {"retry": 2, "empty": 2}
    assert json.loads(jobs_file.read_text()) == {"data": [job("retry")]}
    assert json.loads(current_file.read_text()) == {"retry": 1, "total_jobs": 1}
    assert all(browser.closed for browser in fake_playwright)


def test_parallel_worker_failure_propagates(tmp_path, fake_playwright, monkeypatch):
    def fail_scrape(self, browser, company, progress_info):
        raise RuntimeError("worker failed")

    monkeypatch.setattr(PlaywrightCrawlerRunner, "_scrape_company", fail_scrape)
    runner = PlaywrightCrawlerRunner(
        str(tmp_path / "jobs.json"), str(tmp_path / "current.json"), max_workers=2
    )

    with pytest.raises(RuntimeError, match="worker failed"):
        runner.run([company("first", ScrapeIt), company("second", ScrapeIt)])
    assert all(browser.closed for browser in fake_playwright)


def test_parallel_browser_launch_failure_propagates(tmp_path, fake_playwright, monkeypatch):
    def fail_launch(self, playwright):
        raise RuntimeError("browser launch failed")

    monkeypatch.setattr(PlaywrightCrawlerRunner, "_launch_browser", fail_launch)
    runner = PlaywrightCrawlerRunner(
        str(tmp_path / "jobs.json"), str(tmp_path / "current.json"), max_workers=2
    )

    with pytest.raises(RuntimeError, match="browser launch failed"):
        runner.run([company("first", ScrapeIt), company("second", ScrapeIt)])


def test_parallel_browser_close_failure_propagates(tmp_path, fake_playwright, monkeypatch):
    original_launch = PlaywrightCrawlerRunner._launch_browser

    def launch_with_failing_close(self, playwright):
        browser = original_launch(self, playwright)
        original_close = browser.close

        def fail_close():
            original_close()
            raise RuntimeError("browser close failed")

        browser.close = fail_close
        return browser

    class SuccessfulScraper(ScrapeIt):
        def getJobs(self, page, web_page, company):
            return [job(company)]

    monkeypatch.setattr(PlaywrightCrawlerRunner, "_launch_browser", launch_with_failing_close)
    runner = PlaywrightCrawlerRunner(
        str(tmp_path / "jobs.json"), str(tmp_path / "current.json"), max_workers=2
    )

    with pytest.raises(RuntimeError, match="browser close failed"):
        runner.run([company("first", SuccessfulScraper), company("second", SuccessfulScraper)])
    assert all(browser.closed for browser in fake_playwright)


def test_parallel_write_failure_propagates_and_closes_browsers(tmp_path, fake_playwright, monkeypatch):
    class SuccessfulScraper(ScrapeIt):
        def getJobs(self, page, web_page, company):
            return [job(company)]

    def fail_write(self, company, jobs_data):
        raise OSError("write failed")

    monkeypatch.setattr(PlaywrightCrawlerRunner, "_write_results", fail_write)
    runner = PlaywrightCrawlerRunner(
        str(tmp_path / "jobs.json"), str(tmp_path / "current.json"), max_workers=2
    )

    with pytest.raises(OSError, match="write failed"):
        runner.run([company("first", SuccessfulScraper), company("second", SuccessfulScraper)])
    assert all(browser.closed for browser in fake_playwright)


def test_real_playwright_parallel_matches_sequential(tmp_path):
    class LocalScraper(ScrapeIt):
        def getJobs(self, page, web_page, company):
            page.get(web_page)
            return [{
                "company": company,
                "title": page.find_element(By.CSS_SELECTOR, "h1").text,
                "location": "Remote",
                "link": f"https://example.com/{company}",
            }]

    companies = [
        company(name, LocalScraper, jobs_url=f"data:text/html,{quote(f'<h1>Job at {name}</h1>')}")
        for name in ("first", "second", "third")
    ]
    companies.append(company("headed", LocalScraper, headless=False))
    outputs = []
    for workers in (1, 3):
        jobs_file = tmp_path / f"jobs-{workers}.json"
        current_file = tmp_path / f"current-{workers}.json"
        runner = PlaywrightCrawlerRunner(
            str(jobs_file), str(current_file), max_workers=workers, max_attempts=1
        )
        runner.run(companies)
        outputs.append((json.loads(jobs_file.read_text()), json.loads(current_file.read_text())))

    expected_names = ["first", "second", "third"]
    assert outputs[0] == outputs[1]
    assert outputs[1][0] == {"data": [job(name) for name in expected_names]}
    assert outputs[1][1] == {**dict.fromkeys(expected_names, 1), "total_jobs": 3}
