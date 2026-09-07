import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrape_it import ScrapeIt

# https://www.coinbase.com/careers/positions
class ScrapeCoinbase(ScrapeIt):
    name = 'Coinbase'

    def getJobs(self, driver, web_page, company='coinbase') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        time.sleep(2)
        
        # Handle cookie consent banner with multiple strategies
        try:
            banner_closed = False
            
            # Strategy 1: Remove the cookie banner dialog entirely
            try:
                driver.execute_script("""
                    // Try to find and close cookie banner
                    var banners = document.querySelectorAll('[id*="cookie"], [class*="cookie"], [id*="consent"], [class*="consent"], [role="dialog"]');
                    banners.forEach(function(el) { 
                        try {
                            el.remove();
                        } catch(e) {}
                    });
                """)
                self.log_info("Removed cookie banner elements via JavaScript", company=company)
                banner_closed = True
            except:
                pass
            
            # Strategy 2: Click Accept/Agree button if banner still exists
            if not banner_closed:
                try:
                    # Find and click Accept button
                    driver.execute_script("""
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                            if (buttons[i].textContent.includes('Accept') || buttons[i].textContent.includes('Agree')) {
                                buttons[i].click();
                                break;
                            }
                        }
                    """)
                    self.log_info("Clicked Accept/Agree button via JavaScript search", company=company)
                    banner_closed = True
                except:
                    pass
            
            # Strategy 3: Disable body overflow to show content
            try:
                driver.execute_script("document.body.style.overflow='auto'; document.body.style.height='auto';")
                self.log_info("Enabled body overflow", company=company)
            except:
                pass
            
            time.sleep(2)
                
        except Exception as e:
            self.log_info("Error handling cookie banner", company=company, error=str(e))
        
        # Remove any overlays that might be blocking interaction
        try:
            driver.execute_script("""
                // Remove modal overlays
                var overlays = document.querySelectorAll('[role="dialog"], .modal, .overlay, [aria-modal="true"], [id*="modal"], [class*="modal"]');
                overlays.forEach(function(el) { 
                    try { el.remove(); } catch(e) {}
                });
                
                // Remove backdrop overlays
                var backdrops = document.querySelectorAll('[class*="backdrop"], [id*="backdrop"]');
                backdrops.forEach(function(el) { 
                    try { el.remove(); } catch(e) {}
                });
                
                // Restore body and html
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
                document.body.style.height = 'auto';
            """)
            self.log_info("Removed overlay elements", company=company)
        except:
            pass
        
        time.sleep(1)
        
        # Expand all departments to populate job listings
        try:
            # Get department buttons (the actual clickable elements)
            department_buttons = driver.find_elements(By.XPATH, '//div[@data-testid="positions-department"]//button')
            
            if not department_buttons:
                self.log_info("No department buttons found, trying direct div click", company=company)
                # Fallback to clicking the div directly
                departments = driver.find_elements(By.XPATH, '//div[@data-testid="positions-department"]')
                department_buttons = departments
            else:
                self.log_info(
                    "Department buttons found",
                    company=company,
                    button_count=len(department_buttons),
                    web_page=web_page,
                )
                
                # Click each department button to expand it and load its jobs
                for idx, button in enumerate(department_buttons):
                    try:
                        # Scroll into view before clicking
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(0.3)
                        
                        # Click using JavaScript to expand the department
                        driver.execute_script("arguments[0].click();", button)
                        self.log_info(f"Clicked department button {idx + 1}/{len(department_buttons)}", company=company)
                        
                        # Wait for jobs to load for this department
                        time.sleep(0.8)
                    except Exception as e:
                        self.log_info(f"Error clicking department button {idx + 1}", company=company, error=str(e))
                        pass
                
                self.log_info("All department buttons expanded", company=company)
        except Exception as e:
            self.log_info("Error processing departments", company=company, error=str(e))
        
        # Wait for all job listings to be available
        time.sleep(2)
        
        # DIAGNOSTIC: Check what elements are on the page after clicking departments
        try:
            # Count various element types to understand page structure
            all_links = driver.find_elements(By.TAG_NAME, 'a')
            all_divs = driver.find_elements(By.TAG_NAME, 'div')
            
            # Look for elements with data attributes that might indicate jobs
            job_test_ids = driver.find_elements(By.XPATH, '//*[@data-testid and contains(@data-testid, "job")]')
            position_elements = driver.find_elements(By.XPATH, '//*[@data-testid="positions-job"]')
            
            self.log_info(
                "Diagnostic info after department expansion",
                company=company,
                total_links=len(all_links),
                total_divs=len(all_divs),
                job_testid_elements=len(job_test_ids),
                positions_job_elements=len(position_elements),
            )
            
            # Log a sample of text content from divs that might be jobs
            for div in all_divs[:20]:
                text = div.text.strip()
                if text and len(text) < 80 and ('senior' in text.lower() or 'engineer' in text.lower() or 'developer' in text.lower()):
                    self.log_info(f"  Potential job text: {text}", company=company)
                    
        except Exception as e:
            self.log_info(f"Error during diagnostic: {str(e)[:60]}", company=company)
        
        # Find job links with pattern /careers/positions/{id}
        try:
            job_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/careers/positions/")]')
            self.log_info(f"Found {len(job_links)} job links total", company=company)
            
            # Filter to only actual job links (not navigation)
            group_elements = []
            for link in job_links:
                href = link.get_attribute('href') or ""
                text = link.text.strip()
                
                # Must match pattern /careers/positions/{numeric_id}
                if '/careers/positions/' in href and text and len(text) < 150:
                    # Skip common non-job pages
                    if not any(x in href.lower() for x in ['#', 'back', 'cookie', 'legal']):
                        group_elements.append(link)
            
            self.log_info(f"Filtered to {len(group_elements)} actual job listings", company=company)
            
            # Debug: show first 5 jobs
            for idx, elem in enumerate(group_elements[:5]):
                try:
                    href = elem.get_attribute('href')
                    text = elem.text.strip()[:60]
                    self.log_info(f"  Job {idx + 1}: {text} -> {href}", company=company)
                except:
                    pass
        except Exception as e:
            self.log_info(f"Error finding job links: {str(e)[:50]}", company=company)
        
        result = []
        for i, elem in enumerate(group_elements):
            try:
                job_url = elem.get_attribute('href') or ""
                job_name = elem.text.strip()
                
                # Only accept links that point to actual job positions (must have /careers/positions/ in URL)
                if not job_url or '/careers/positions/' not in job_url:
                    continue
                
                # Skip common footer/navigation links
                excluded_patterns = ['/login', '/signup', '/about', '/blog', '/press', '/security', 
                                   '/investors', '/vendors', '/legal', '/cookie', '/affiliates',
                                   '/terms', '/privacy', 'e-verify', 'eeoc', 'chromevox']
                
                if any(pattern in job_url.lower() for pattern in excluded_patterns):
                    continue
                    
                if any(pattern in job_name.lower() for pattern in excluded_patterns):
                    continue
                
                # Skip if missing job name
                if not job_name:
                    continue
                
                # Try to extract location from parent elements
                location = "Remote"  # Default location
                try:
                    parent = elem.find_element(By.XPATH, '..')
                    parent_text = parent.text.strip()
                    
                    # Look for location info in parent siblings or descendants
                    lines = parent_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and line != job_name and not line.startswith('http') and len(line) < 100:
                            location = line
                            break
                except:
                    pass
                
                job = {
                    "company": company,
                    "title": job_name,
                    "location": location,
                    "link": job_url
                }
                result.append(job)
            except Exception as e:
                continue
        
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(group_elements),
            jobs_scraped=len(result),
        )
        return result
