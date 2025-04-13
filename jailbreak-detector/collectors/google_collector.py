from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import re
from analyzers.prompt_analyzer import PromptAnalyzer
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleCollector:
    def __init__(self):
        # Just one test query
        self.search_queries = [
            "DAN jailbreak prompt example"  # More specific query likely to find actual prompts
        ]
        
        # Headers to mimic a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Keywords that might indicate jailbreak discussions
        self.keywords = [
            "jailbreak",
            "adversarial prompt",
            "bypass",
            "security measure",
            "prompt injection",
            "DAN",  # Do Anything Now
            "system prompt"
        ]

        self.analyzer = PromptAnalyzer()

        # Chrome setup should be here, right after the analyzer
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run in background
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")

    def _search_google(self, query: str, num_pages: int = 1) -> List[str]:
        """Get URLs from Google search results using Selenium"""
        all_urls = []
        
        # Enhanced Chrome options
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        wait = WebDriverWait(driver, 10)
        
        try:
            for page in range(num_pages):
                search_url = f"https://www.google.com/search?q={quote_plus(query)}&start={page * 10}"
                print(f"\nSearching page {page + 1}: {search_url}")
                
                driver.get(search_url)
                time.sleep(random.uniform(2, 4))  # Random delay
                
                # Updated selectors based on current Google HTML structure
                selectors = [
                    "div.g a[href^='http']",  # Basic link selector
                    "div.yuRUbf a[href^='http']",  # Another common pattern
                    "div.rc a[href^='http']",  # Alternative format
                    "div.tF2Cxc a[href^='http']"  # Another variation
                ]
                
                # Scroll down slowly to mimic human behavior
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                for selector in selectors:
                    try:
                        # Wait for elements to be present
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        links = driver.find_elements(By.CSS_SELECTOR, selector)
                        print(f"Found {len(links)} links with selector: {selector}")
                        
                        for link in links:
                            try:
                                # Get href using JavaScript to avoid detection
                                url = driver.execute_script("return arguments[0].getAttribute('href');", link)
                                if url and url.startswith("http") and url not in all_urls:
                                    all_urls.append(url)
                                    print(f"Found URL: {url}")
                            except Exception as e:
                                continue
                            
                    except Exception as e:
                        continue
                
                if not all_urls:
                    print("No results found with any selector, trying alternative approach...")
                    try:
                        # Try getting all links and filter
                        all_links = driver.find_elements(By.TAG_NAME, "a")
                        for link in all_links:
                            url = link.get_attribute("href")
                            if url and url.startswith("http") and "google" not in url:
                                if url not in all_urls:
                                    all_urls.append(url)
                                    print(f"Found URL (alternative): {url}")
                    except Exception as e:
                        print(f"Alternative approach failed: {str(e)}")
                
                time.sleep(random.uniform(2, 4))  # Random delay between pages
                
        except Exception as e:
            print(f"Error during search: {str(e)}")
            
        finally:
            driver.quit()
            
        print(f"\nTotal URLs found: {len(all_urls)}")
        return all_urls

    def _extract_content(self, url: str) -> str:
        """Extract text content from a URL"""
        try:
            print(f"\nTrying to extract content from: {url}")
            
            # Add more browser-like headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Response status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Focus on main content areas
            content_tags = soup.find_all(['article', 'main', 'div', 'p'])
            print(f"Found {len(content_tags)} content tags")
            
            text_content = []
            for tag in content_tags:
                # Skip navigation, headers, footers
                if tag.parent and tag.parent.name in ['nav', 'header', 'footer']:
                    continue
                
                # Get text and preserve structure
                text = tag.get_text('\n', strip=True)
                if text:
                    text_content.append(text)
            
            final_text = '\n'.join(text_content)
            print(f"Extracted {len(final_text)} characters of text")
            return final_text
            
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return ""

    def _find_relevant_sections(self, text: str) -> List[Dict[str, Any]]:
        """Find sections of text containing keywords"""
        sections = []
        
        # Debug: Print total text length
        print(f"\nTotal text length: {len(text)}")
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        print(f"Found {len(paragraphs)} paragraphs")
        
        for i, paragraph in enumerate(paragraphs):
            # Debug: Print each paragraph we're checking
            print(f"\nChecking paragraph {i}: {paragraph[:100]}...")
            
            # Check if paragraph contains any keywords
            found_keywords = [k for k in self.keywords if k.lower() in paragraph.lower()]
            if found_keywords:
                print(f"Found keywords: {found_keywords}")
                # Get surrounding context
                start = max(0, i-1)
                end = min(len(paragraphs), i+2)
                context = '\n\n'.join(paragraphs[start:end])
                
                sections.append({
                    "text": paragraph,
                    "context": context
                })
                print(f"Added section with length: {len(paragraph)}")
        
        print(f"\nTotal relevant sections found: {len(sections)}")
        return sections

    def collect(self) -> List[Dict[str, Any]]:
        """Collect and analyze potential jailbreak content"""
        all_sections = []
        verified_jailbreaks = []
        
        for query in self.search_queries:
            print(f"\nSearching for: {query}")
            urls = self._search_google(query)
            
            # Only process first 2 URLs for testing
            for url in urls[:2]:  # Added limit here
                print(f"\nAnalyzing: {url}")
                content = self._extract_content(url)
                
                if content:
                    sections = self._find_relevant_sections(content)
                    for section in sections:
                        section["source_url"] = url
                        section["search_query"] = query
                    all_sections.extend(sections)
                
                time.sleep(2)

        # Have Claude analyze each section
        print(f"\nAnalyzing {len(all_sections)} relevant sections...")
        for section in all_sections:
            analysis = self.analyzer.analyze_prompt(
                prompt_text=section["text"],
                context=section["context"]
            )
            if analysis and analysis["is_adversarial"]:
                analysis["source_url"] = section["source_url"]
                verified_jailbreaks.append(analysis)
                print(f"\nFound jailbreak content!")
                print(f"Text: {section['text'][:200]}...")
                print(f"Type: {analysis['attack_type']}")
                print(f"Severity: {analysis['severity']}")

        return verified_jailbreaks 