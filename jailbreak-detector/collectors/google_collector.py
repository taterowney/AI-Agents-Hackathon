from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import re
from analyzers.prompt_analyzer import PromptAnalyzer
import random

class GoogleCollector:
    def __init__(self):
        # General search queries for finding jailbreak prompts
        self.search_queries = [
            "successful jailbreak prompts examples",
            "LLM adversarial prompt bypass",
            "ChatGPT jailbreak techniques",
            "AI safety bypass prompts"
        ]
        
        # Headers to mimic a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Patterns to identify prompts in text
        self.prompt_patterns = [
            r'(?:prompt:|input:)\s*["\'](.*?)["\']',
            r'(?:Human|User|System):\s*(.*?)(?:\n|Assistant:|$)',
            r'<prompt>(.*?)</prompt>',
            r'```\s*prompt\s*\n(.*?)\n```',
            r'Example\s*\d*:\s*(.*?)(?:\n\n|$)'
        ]

        self.analyzer = PromptAnalyzer()

    def _search_google(self, query: str, num_pages: int = 5) -> List[str]:
        """Get URLs from multiple pages of Google search results"""
        all_urls = []
        
        for page in range(num_pages):
            start_index = page * 10  # Google shows 10 results per page
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&start={start_index}"
            
            try:
                # Random delay between requests (3-7 seconds)
                delay = 3 + random.random() * 4
                time.sleep(delay)
                
                response = requests.get(search_url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract result URLs
                    for result in soup.find_all('a'):
                        href = result.get('href', '')
                        if href.startswith('/url?q='):
                            url = href.split('/url?q=')[1].split('&')[0]
                            if url not in all_urls:  # Avoid duplicates
                                all_urls.append(url)
                                print(f"Found URL: {url}")
                else:
                    print(f"Search failed with status code: {response.status_code}")
                    break  # Stop if we hit an error
                
            except Exception as e:
                print(f"Error searching Google (page {page+1}): {str(e)}")
                break
        
        return all_urls

    def _extract_content(self, url: str) -> str:
        """Extract text content from a URL"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
                
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            text = ' '.join(line for line in lines if line)
            
            return text
            
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return ""

    def _extract_prompts(self, text: str) -> List[Dict[str, Any]]:
        """Extract potential prompts from text"""
        prompts = []
        
        for pattern in self.prompt_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                prompt_text = match.group(1).strip()
                if len(prompt_text) > 20:  # Filter out very short matches
                    # Get surrounding context
                    start = max(0, match.start() - 200)
                    end = min(len(text), match.end() + 200)
                    context = text[start:end]
                    
                    prompts.append({
                        "text": prompt_text,
                        "context": context,
                        "source_pattern": pattern
                    })
        
        return prompts

    def collect(self) -> List[Dict[str, Any]]:
        """Collect and analyze jailbreak prompts"""
        all_prompts = []
        verified_prompts = []
        
        # First collect potential prompts
        for query in self.search_queries:
            print(f"\nSearching for: {query}")
            urls = self._search_google(query)
            
            for url in urls:
                print(f"Analyzing: {url}")
                content = self._extract_content(url)
                prompts = self._extract_prompts(content)
                all_prompts.extend(prompts)
                
                # Be nice to servers
                time.sleep(2)

        # Then analyze each prompt
        print(f"\nAnalyzing {len(all_prompts)} potential prompts...")
        for prompt in all_prompts:
            analysis = self.analyzer.analyze_prompt(
                prompt_text=prompt["text"],
                context=prompt["context"]
            )
            if analysis and analysis["is_adversarial"]:
                analysis["source_url"] = prompt["source_url"]
                analysis["search_query"] = prompt["search_query"]
                verified_prompts.append(analysis)
                print(f"\nFound adversarial prompt!")
                print(f"Type: {analysis['attack_type']}")
                print(f"Severity: {analysis['severity']}")
                print(f"Reason: {analysis['reason']}")

        print(f"\nFound {len(verified_prompts)} verified adversarial prompts")
        return verified_prompts 