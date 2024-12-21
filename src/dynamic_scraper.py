from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import create_key

def scrape_from_2016(year):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        return {}

    try:
        all_org_data = {}
        base_url = f"https://summerofcode.withgoogle.com/archive/{year}/organizations"
        
        try:
            driver.get(base_url)
        except WebDriverException as e:
            print(f"Error accessing the base URL {base_url}: {e}")
            return {}
        
        try:
            WebDriverWait(driver, 4).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
                )
                   
        except TimeoutException:
            print("Timeout waiting for organization names to load.")
        
        current_num = 0;        
        
        while True:
            # Fetch organization names and links
            try:
                elements_names = driver.find_elements(By.CLASS_NAME, "name")
                filtered_links = [
                    el.get_attribute("href")
                    for el in driver.find_elements(By.CSS_SELECTOR, "a[href*='/archive/']")
                ]
            except NoSuchElementException as e:
                print(f"Error finding elements on the page: {e}")
                break

            # Use a thread pool to scrape details concurrently
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(scrape_details, link): name.text
                    for name, link in zip(elements_names, filtered_links)
                }

                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        technologies, topics = future.result()
                        technologies = str(technologies).replace(",", " | ")
                        topics = str(topics).replace(",", " | ")

                        # 
                        # print(name, technologies, topics)
                        
                        # Counter
                        current_num+=1
                        print(f"\r{current_num}", end="", flush=True)
                                                
                        all_org_data[create_key(name)] = {
                            "name": name,
                            "technologies": technologies,
                            "topics": topics,
                        }
                    except Exception as e:
                        print(f"Error processing {name}: {e}")

            # Check if the "Next" button is disabled
            try:
                next_button = driver.find_element(By.CLASS_NAME, "mat-mdc-paginator-navigation-next")
                is_disabled = next_button.get_attribute("disabled")
            except NoSuchElementException:
                print("\nNext button not found. Assuming last page.")
                break

            if is_disabled:
                print("\nReached the last page.")
                break

            # Click the "Next" button and wait for the page to refresh
            try:
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, 4).until(EC.staleness_of(elements_names[0]))
            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                break

        return all_org_data
    finally:
        driver.quit()

def scrape_details(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    try:
        detail_driver = webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"Error initializing detail WebDriver: {e}")
        return "", ""

    try:
        try:
            detail_driver.get(url)
        except WebDriverException as e:
            print(f"Error accessing detail page {url}: {e}")
            return "", ""

        try:
            WebDriverWait(detail_driver, 4).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "tech__content"))
            )
        except TimeoutException:
            print(f"Timeout waiting for details to load on page {url}")
            return "", ""

        try:
            technologies = detail_driver.find_element(By.CLASS_NAME, "tech__content").text
            topics = detail_driver.find_element(By.CLASS_NAME, "topics__content").text
        except NoSuchElementException as e:
            print(f"Error finding details on page {url}: {e}")
            return "", ""

        return technologies, topics
    finally:
        detail_driver.quit()

# if __name__ == "__main__":
#     try:
#         data = scrape_from_2016(2023)
#     except Exception as e:
#         print(f"Unexpected error: {e}")


