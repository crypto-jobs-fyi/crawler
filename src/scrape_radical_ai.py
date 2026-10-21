from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightPageAdapter, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeRadicalAI(ScrapeIt):
    name = "RADICAL_AI"
    _job_link_selector = 'a[href*="/jobs/public/"]'

    def _extract_jobs(self, page: PlaywrightPageAdapter) -> list[dict]:
        return page.execute_script(
            """
            const selector = arguments[0];
            return Array.from(document.querySelectorAll(selector)).map((link) => {
              const content = link.firstElementChild;
              const titleElement = content?.firstElementChild;
              const metadataElement = content?.lastElementChild;
              const locationElement = metadataElement?.firstElementChild;
              return {
                href: link.href,
                title: (
                  titleElement?.textContent
                  || link.textContent
                  || ''
                ).replace(/\\s+/g, ' ').trim(),
                location: (
                  locationElement?.textContent
                  || ''
                ).replace(/\\s+/g, ' ').trim(),
              };
            });
            """,
            self._job_link_selector,
        ) or []

    def getJobs(
        self,
        page: PlaywrightPageAdapter,
        web_page: str,
        company: str,
    ) -> list:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.implicitly_wait(10)
        page.get(web_page)

        try:
            PlaywrightWait(page, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self._job_link_selector)
                )
            )
        except TimeoutError:
            self.log_warning(
                "No Radical AI job links found before timeout",
                company=company,
                web_page=web_page,
            )
            return []

        jobs_by_url = {}
        for item in self._extract_jobs(page):
            job_url = (item.get("href") or "").strip()
            title = (item.get("title") or "").strip()
            if not job_url or not title or job_url in jobs_by_url:
                continue
            jobs_by_url[job_url] = {
                "company": company,
                "title": title,
                "location": (item.get("location") or "").strip() or "Unknown",
                "link": job_url,
            }

        result = list(jobs_by_url.values())
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(jobs_by_url),
            jobs_scraped=len(result),
        )
        return result
