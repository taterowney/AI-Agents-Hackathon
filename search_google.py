from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests

def search_google_and_get_top_pages(query, num_pages=5):
    # Set up Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.google.com")
        time.sleep(2)

        # Accept cookies if necessary
        try:
            consent_button = driver.find_element(By.XPATH, '//button/div[contains(text(), "Accept all")]')
            consent_button.click()
            time.sleep(1)
        except Exception:
            pass  # No consent form

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # More robust way to get search result links
        link_elements = driver.find_elements(By.XPATH, '//a[@href and @data-ved]')
        urls = []
        for link in link_elements:
            href = link.get_attribute('href')
            if href.startswith('http') and "google.com" not in href:
                urls.append(href)
            if len(urls) >= num_pages:
                break

    finally:
        driver.quit()

    page_texts = []

    # Fetch the content of each page
    for url in urls:
        try:
            print(f"Fetching {url}...")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            page_texts.append((url, text))
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            page_texts.append((url, ""))

    return page_texts

    return page_texts
