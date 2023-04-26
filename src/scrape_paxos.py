from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs


def to_records(group_elements, company) -> []:
    result = []
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        job = {
            "company": company,
            "title": elem.text,
            "location": 'US',
            "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
        }
        result.append(job)
    return result


class ScrapePaxos(ScrapeIt):
    def getJobs(self, driver, web_page, company='paxos') -> []:
        print(f'[PAXOS] Scrap page: {web_page}')
        driver.get(web_page)
        next_link = 'a[class="page-numbers"]'
        next_links = driver.find_elements(By.CSS_SELECTOR, next_link)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'h3 a[href]')
        result = to_records(group_elements, company)
        i = 1
        for nxt in next_links:
            i += 1
            driver.get(f'{web_page}&sf_paged={i}')
            group_elements = driver.find_elements(By.CSS_SELECTOR, 'h3 a[href]')
            result += to_records(group_elements, company)

        print(f'[PAXOS] Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
