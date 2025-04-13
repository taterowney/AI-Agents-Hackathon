from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
from analyzers.prompt_analyzer import PromptAnalyzer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class GoogleCollector:
    def __init__(self):
        # Two test queries
        self.search_queries = [
            "DAN jailbreak prompt example",
            "Grok AI Jailbreak prompts",
            "LLAMA jailbreak prompts" # Adding another specific query
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

        # Enhanced Chrome options to better avoid detection
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless=new')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--disable-infobars')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)

    def _search_google(self, query: str) -> List[str]:
        """Get first 3 URLs from Google search results"""
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        found_urls = []
        
        try:
            # Stealth setup
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            print(f"\nSearching: {search_url}")
            
            driver.get(search_url)
            time.sleep(3)  # Initial wait
            
            # Scroll a bit like a human
            driver.execute_script("window.scrollTo(0, 200)")
            time.sleep(1)
            
            # Try multiple selectors to find results
            selectors = [
                "//div[@class='yuRUbf']//a[@href]",  # Modern Google format
                "//div[@class='g']//a[@href]",        # Alternative format
                "//div[@class='rc']//a[@href]"        # Older format
            ]
            
            for selector in selectors:
                if len(found_urls) >= 3:  # Changed back to 3
                    break
                    
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        url = element.get_attribute('href')
                        if url and url.startswith('http') and 'google' not in url:
                            if url not in found_urls:
                                found_urls.append(url)
                                print(f"Found URL {len(found_urls)}: {url}")
                                if len(found_urls) >= 3:  # Changed back to 3
                                    break
                except Exception as e:
                    print(f"Error with selector {selector}: {e}")
                    continue
                
            return found_urls[:3]  # Return up to 3 URLs
        
        except Exception as e:
            print(f"Error during search: {e}")
        finally:
            driver.quit()

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
        all_prompts = []
        
        # Process each search query
        for query in self.search_queries:
            print(f"\nSearching for: {query}")
            urls = self._search_google(query)
            
            print(f"\nFound {len(urls)} URLs to analyze for query: {query}")
            
            for url in urls:
                print(f"\nAnalyzing: {url}")
                content = self._extract_content(url)
                
                if content:
                    analysis = self.analyzer.analyze_prompt(
                        prompt_text=content,
                        source_url=url
                    )
                    if analysis:
                        print(f"Found prompts in {url}")
                        for prompt in analysis:
                            prompt["source_url"] = url
                            prompt["search_query"] = query  # Add query info
                            all_prompts.append(prompt)

        print(f"\nTotal prompts found across all queries: {len(all_prompts)}")
        return all_prompts 