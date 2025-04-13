import time
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def google_search(query):
    """
    Uses Selenium to search Google for the given query and returns the URLs of the top 5 results.
    """
    # Set up Chrome to run in headless mode
    options = Options()
    options.add_argument("--headless")
    # Optional: add other options like user-agent if needed.

    # Initialize the WebDriver (make sure chromedriver is installed and in PATH)
    driver = webdriver.Chrome(options=options)

    # Encode the query and navigate to the search results page.
    search_url = f"https://www.google.com/search?q={query}"
    driver.get(search_url)

    # Wait for the page to load. (Adjust the sleep delay if necessary.)
    time.sleep(3)

    # Locate result elements using CSS selectors.
    # Google typically wraps each link in a <div class="yuRUbf"> element.
    result_elements = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")

    urls = []
    for element in result_elements:
        href = element.get_attribute("href")
        if href:
            urls.append(href)
        if len(urls) >= 5:
            break

    driver.quit()
    return urls


def get_page_content(url):
    """
    Fetches the content of a given URL using the requests library and parses it with BeautifulSoup.
    Returns the text content of the page.
    """
    try:
        # Use a common browser user-agent to help avoid blocks.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse using BeautifulSoup with the built-in HTML parser.
        soup = BeautifulSoup(response.text, "html.parser")
        # You can further refine what "content" to extract.
        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        return f"Error retrieving {url}: {e}"

#
# def main():
#     # Get the search query from command-line arguments, default to "OpenAI ChatGPT"
#     if len(sys.argv) > 1:
#         query = sys.argv[1]
#     else:
#         query = "OpenAI ChatGPT"
#
#     print(f"Searching Google for: {query}")
#
#     # Get the top 5 search result URLs.
#     urls = google_search(query)
#     print("\nTop 5 URLs:")
#     for idx, url in enumerate(urls, start=1):
#         print(f"{idx}. {url}")
#
#     # For each URL, fetch and extract page content using BeautifulSoup.
#     for idx, url in enumerate(urls, start=1):
#         print(f"\nExtracting content from URL {idx}: {url}")
#         content = get_page_content(url)
#         # For demonstration, print the first 1000 characters of the content.
#         print(content[:1000])
#         print("\n" + "=" * 80 + "\n")

