import src.scrape_greenhouse as greenhouse
from src.playwright_adapter import By
from src.scrape_greenhouse import ScrapeGreenhouse


def test_live_xai_pagination_includes_sixth_page(page_adapter):
    base_url = "https://job-boards.greenhouse.io/xai"
    page_adapter.get(f"{base_url}?page=6")
    sixth_page_jobs = greenhouse.get_jobs(page_adapter, "xai")
    assert sixth_page_jobs, "Expected xAI jobs on page 6"
    last_page = not page_adapter.find_elements(By.XPATH, ScrapeGreenhouse._next_page_selector)

    from_sixth_page = ScrapeGreenhouse().getJobs(page_adapter, f"{base_url}?page=6", "xai")
    if last_page:
        assert from_sixth_page == sixth_page_jobs

    jobs = ScrapeGreenhouse().getJobs(page_adapter, base_url, "xai")
    links = [job["link"] for job in jobs]
    assert len(links) == len(set(links)), "Pagination returned duplicate jobs"
    assert {job["link"] for job in sixth_page_jobs}.issubset(links)
