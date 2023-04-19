from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs


def clean_location(location):
    locations = set(filter(None, ([x.strip() for x in location.split(',')])))
    if len(locations) == 1:
        return next(iter(locations)).strip().lstrip('-').title()
    joined = ' '.join(locations).lower()
    if joined.count('remote') > 1:
        return joined.replace('remote', '', 1).strip().lstrip('-').title()
    return joined.strip().lstrip('-').title()


class ScrapeLever(ScrapeIt):
    def getJobs(self, driver, web_page, company) -> []:
        print(f'[LEVER] Scrap page: {web_page}')
        driver.get(web_page)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'a[class="posting-title"]')
        print(f'[LEVER] Found {len(group_elements)} jobs.')
        result = []
        for elem in group_elements:
            link_elem = elem.find_element(By.CSS_SELECTOR, '[data-qa="posting-name"]')
            location_elem = elem.find_elements(By.CSS_SELECTOR, '[class*="location"]')
            workplace_elem = elem.find_elements(By.CSS_SELECTOR, '[class*="workplaceTypes"]')
            job_url = elem.get_attribute('href')
            if len(location_elem) > 0:
                location = location_elem[0].text
            else:
                location = ''
            if len(workplace_elem) > 0:
                workplace = workplace_elem[0].text
                merge_location = f'{location},{workplace}'
            else:
                merge_location = location
            job = {
                "company": company,
                "title": link_elem.text,
                "location": clean_location(merge_location),
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[LEVER]  Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
