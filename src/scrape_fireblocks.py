from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightPageAdapter, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeFireblocks(ScrapeIt):
    name = "FIREBLOCKS"
    _job_link_selector = (
        'div.careers-job[data-job-title] '
        'a[href*="/careers/positions/"]'
    )

    @staticmethod
    def _dismiss_consent(page: PlaywrightPageAdapter) -> None:
        buttons = page.find_elements(
            By.XPATH,
            '//button[normalize-space(.)="Accept All"]',
        )
        for button in buttons:
            if button.is_displayed():
                button.click()
                return

    @staticmethod
    def _expand_departments(page: PlaywrightPageAdapter) -> None:
        page.execute_script(
            """
            for (const button of document.querySelectorAll(
              'button.careers-department__toggle[aria-expanded="false"]'
            )) {
              button.click();
            }
            """
        )

    def _extract_jobs(self, page: PlaywrightPageAdapter) -> list[dict]:
        return page.execute_script(
            """
            const selector = arguments[0];
            return Array.from(document.querySelectorAll(selector)).map((link) => {
              const card = link.closest('.careers-job');
              const locationElement = card
                ? card.querySelector('.careers-job__location')
                : null;
              return {
                href: link.href,
                title: (link.textContent || '').replace(/\\s+/g, ' ').trim(),
                location: (
                  locationElement?.textContent
                  || card?.getAttribute('data-job-location')
                  || ''
                ).replace(/\\s+/g, ' ').trim(),
              };
            });
            """,
            self._job_link_selector,
        ) or []

    @staticmethod
    def _page_signature(page: PlaywrightPageAdapter, selector: str) -> str:
        return page.execute_script(
            """
            const selector = arguments[0];
            return Array.from(document.querySelectorAll(selector))
              .map((link) => link.href)
              .join('|');
            """,
            selector,
        ) or ""

    def _advance_page(
        self,
        page: PlaywrightPageAdapter,
        previous_signature: str,
    ) -> bool:
        clicked = page.execute_script(
            """
            const candidates = Array.from(document.querySelectorAll('button, a'));
            const next = candidates.find((element) => {
              const text = [
                element.getAttribute('aria-label') || '',
                element.getAttribute('title') || '',
                element.textContent || '',
              ].join(' ').replace(/\\s+/g, ' ').trim().toLowerCase();
              return /(^|\\s)(next( page)?|load more)(\\s|$)/.test(text)
                && element.offsetParent !== null
                && !element.disabled
                && element.getAttribute('aria-disabled') !== 'true';
            });
            if (!next) {
              return false;
            }
            next.click();
            return true;
            """
        )
        if not clicked:
            return False

        try:
            PlaywrightWait(page, 20).until(
                lambda current_page: self._page_signature(
                    current_page,
                    self._job_link_selector,
                )
                != previous_signature
            )
        except TimeoutError:
            self.log_warning("Fireblocks pagination did not load a new page")
            return False
        return True

    def getJobs(
        self,
        page: PlaywrightPageAdapter,
        web_page: str,
        company: str,
    ) -> list:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.implicitly_wait(10)
        page.get(web_page)
        self._dismiss_consent(page)

        try:
            PlaywrightWait(page, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self._job_link_selector)
                )
            )
        except TimeoutError:
            self.log_warning(
                "No Fireblocks job links found before timeout",
                company=company,
                web_page=web_page,
            )
            return []

        self._expand_departments(page)
        jobs_by_url = {}
        pages_scraped = 0
        while pages_scraped < 50:
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

            pages_scraped += 1
            if not self._advance_page(
                page,
                self._page_signature(page, self._job_link_selector),
            ):
                break

        result = list(jobs_by_url.values())
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(jobs_by_url),
            jobs_scraped=len(result),
            pages_scraped=pages_scraped,
        )
        return result
