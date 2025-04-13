from typing import List, Dict, Any
import arxiv
from datetime import datetime
import time
import requests
import PyPDF2
import io
import re
import anthropic
import os

class ArxivCollector:
    def __init__(self):
        # Search queries for relevant papers
        self.search_queries = [
            'title:"jailbreak" AND "large language model"',
            'title:"prompt injection" AND "LLM"',
            'abs:"adversarial prompts" AND "ChatGPT"',
            'abs:"prompt attack" AND "language model"'
        ]
        
        # Maximum results per query
        self.max_results = 100
        
        # Keywords to look for in abstracts
        self.relevant_keywords = [
            "jailbreak",
            "prompt injection",
            "adversarial prompt",
            "security bypass",
            "model manipulation",
            "prompt attack"
        ]
        
        # Configure arxiv client
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,  # Be nice to ArXiv API
            num_retries=3
        )

        # Patterns to identify prompts in papers
        self.prompt_patterns = [
            r'(?:prompt|query|input):\s*["\'](.*?)["\']',  # Quoted prompts
            r'(?:Human|User|System):\s*(.*?)(?:\n|$)',     # Conversation format
            r'<prompt>(.*?)</prompt>',                      # XML-style tags
            r'```prompt\n(.*?)```',                        # Markdown code blocks
            r'Example \d+[:.]\s*(.*?)(?:\n|$)'            # Example listings
        ]

        # Initialize Anthropic client
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_key:
            raise ValueError("Anthropic API key not found in environment variables")
            
        # Basic client initialization
        self.claude = anthropic.Anthropic(api_key=self.anthropic_key)
        
        # More concise system prompt
        self.system_prompt = """Analyze academic paper excerpts to identify genuine jailbreak prompts. 
        Only flag prompts that were explicitly demonstrated to successfully bypass AI safety measures."""

    def _is_relevant(self, paper: arxiv.Result) -> bool:
        """Check if paper is relevant based on title and abstract"""
        text = (paper.title + " " + paper.summary).lower()
        return any(keyword.lower() in text for keyword in self.relevant_keywords)

    def _extract_prompts_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract prompts from text content"""
        prompts = []
        
        for pattern in self.prompt_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                prompt_text = match.group(1).strip()
                if len(prompt_text) > 20:  # Filter out very short matches
                    prompt = {
                        "text": prompt_text,
                        "pattern_matched": pattern,
                        "context": text[max(0, match.start()-100):match.end()+100]  # Surrounding context
                    }
                    prompts.append(prompt)
        
        return prompts

    def _download_and_extract_pdf(self, pdf_url: str) -> str:
        """Download and extract text from PDF"""
        try:
            response = requests.get(pdf_url)
            pdf_file = io.BytesIO(response.content)
            
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            print(f"Error extracting PDF: {str(e)}")
            return ""

    def _analyze_prompt_with_claude(self, prompt_text: str, context: str) -> Dict[str, Any]:
        """Have Claude analyze a single prompt with its context"""
        try:
            message = self.claude.messages.create(
                model="claude-3-haiku-20240307",  # Switched to Haiku model
                max_tokens=300,  # Further reduced tokens
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": f"""Paper context: {context[:300]}
Analyze prompt: {prompt_text[:200]}
Is this a proven jailbreak? JSON response:
{{
    "is_jailbreak": true/false,
    "type": "brief type",
    "target": "model",
    "why": "1-2 words"
}}"""
                }]
            )
            
            # Parse response
            try:
                analysis = message.content[0].text
                # Extract JSON from response
                import json
                start_idx = analysis.find('{')
                end_idx = analysis.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    result = json.loads(analysis[start_idx:end_idx])
                    if result.get('is_jailbreak', False):
                        return {
                            "prompt_text": prompt_text,
                            "type": result.get('type', 'Unknown'),
                            "target_llm": result.get('target', 'Not specified'),
                            "success_rate": result.get('success', 'Not mentioned'),
                            "reason": result.get('why', '')
                        }
            except Exception as e:
                print(f"Error parsing response: {str(e)}")
            
            return None
                
        except Exception as e:
            print(f"Error calling API: {str(e)}")
            return None

    def _extract_prompt_data(self, paper: arxiv.Result) -> Dict[str, Any]:
        """Extract and analyze prompts from paper"""
        paper_data = {
            "title": paper.title,
            "abstract": paper.summary,
            "authors": [author.name for author in paper.authors],
            "published": paper.published.isoformat(),
            "url": paper.entry_id,
            "pdf_url": paper.pdf_url,
            "keywords_found": [
                keyword for keyword in self.relevant_keywords
                if keyword.lower() in (paper.title + " " + paper.summary).lower()
            ],
            "verified_jailbreaks": []  # Only store verified jailbreaks
        }
        
        # Extract text from PDF
        print(f"\nAnalyzing paper: {paper.title}")
        pdf_text = self._download_and_extract_pdf(paper.pdf_url)
        if pdf_text:
            # First extract potential prompts
            potential_prompts = self._extract_prompts_from_text(pdf_text)
            print(f"Found {len(potential_prompts)} potential prompts to analyze")
            
            # Have Claude analyze each prompt
            for prompt in potential_prompts:
                analysis = self._analyze_prompt_with_claude(
                    prompt_text=prompt['text'],
                    context=prompt['context']
                )
                if analysis:
                    paper_data["verified_jailbreaks"].append(analysis)
                    print("\nVerified jailbreak found!")
                    print(f"Prompt: {analysis['prompt_text'][:100]}...")
                    print(f"Type: {analysis['type']}")
                    print(f"Target: {analysis['target_llm']}")
                    print(f"Success Rate: {analysis['success_rate']}")
                    print(f"Reason: {analysis['reason']}")
            
            print(f"\nFound {len(paper_data['verified_jailbreaks'])} verified jailbreaks in this paper")
        
        return paper_data

    def collect(self) -> List[Dict[str, Any]]:
        """Collect relevant papers from ArXiv"""
        collected_papers = []
        
        for query in self.search_queries:
            print(f"\nSearching ArXiv for: {query}")
            try:
                search = arxiv.Search(
                    query=query,
                    max_results=self.max_results,
                    sort_by=arxiv.SortCriterion.SubmittedDate
                )
                
                for paper in self.client.results(search):
                    if self._is_relevant(paper):
                        paper_data = self._extract_prompt_data(paper)
                        collected_papers.append(paper_data)
                        print(f"Found relevant paper: {paper.title}")
                        
                # Be nice to ArXiv API
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
                continue
        
        print(f"\nTotal papers collected: {len(collected_papers)}")
        return collected_papers 