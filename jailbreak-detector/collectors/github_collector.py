from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import base64
from dotenv import load_dotenv
from github import Github, Repository, ContentFile, Auth
import logging

class GitHubCollector:
    def __init__(self):
        # Initialize with GitHub token and setup logging
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token not found in environment variables")
        
        # Use the new authentication method
        auth = Auth.Token(self.github_token)
        self.github = Github(auth=auth)
        
        # Keywords to search for in content
        self.keywords = [
            "jailbreak",
            "prompt injection",
            "system prompt",
            "DAN",
            "adversarial prompt",
            "prompt leak",
            "LLM attack",
            "model bypass",
            "security vulnerability",
            "prompt engineering"
        ]
        
        # Focus only on known jailbreak repositories
        self.primary_repos = [
            ("L1B3RT4S/L1B3RT4S", "main"),  # Primary jailbreak collection
            ("LLM-Attacks/LLM-Attacks", "main"),  # Academic research on attacks
            ("yahma/llm-jailbreak-collection", "master"),  # Curated jailbreak collection
            ("jailbreakchat/jailbreak-prompts", "main"),  # Specific jailbreak prompts
        ]
        
        # More specific search terms to find actual jailbreak content
        self.search_terms = [
            "filename:jailbreak.md DAN prompt",
            "path:/prompts filename:*.md jailbreak ChatGPT",
            "filename:collection.md jailbreak stars:>10",
        ]
        
        # Better prompt identification patterns
        self.prompt_patterns = [
            "User:",
            "Human:",
            "Assistant:",
            "System:",
            "DAN",
            "<|",
            "PROMPT:",
            "Instructions:",
            "Query:"
        ]
        
        # Required keywords for actual jailbreak content
        self.required_keywords = [
            "jailbreak",
            "DAN",
            "ignore previous",
            "you are free",
            "bypass",
            "restrictions"
        ]
        
        self.max_repos_per_search = 5  # Reduced from 10
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for debugging and monitoring"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='github_collector.log'
        )
        self.logger = logging.getLogger(__name__)

    def _check_rate_limit(self):
        """Monitor GitHub API rate limits"""
        rate_limit = self.github.get_rate_limit()
        if rate_limit.core.remaining < 100:
            self.logger.warning(f"GitHub API rate limit low: {rate_limit.core.remaining} remaining")
            return False
        return True

    def _extract_content(self, file: ContentFile) -> Optional[str]:
        """Extract and decode content from GitHub file"""
        try:
            if file.encoding == 'base64':
                return base64.b64decode(file.content).decode('utf-8')
            return file.decoded_content.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error decoding file {file.path}: {str(e)}")
            return None

    def _contains_relevant_content(self, content: str) -> bool:
        """Check if content contains relevant keywords"""
        content_lower = content.lower()
        
        # Check for required keywords (need at least one)
        has_required = any(keyword.lower() in content_lower 
                         for keyword in self.required_keywords)
                         
        # Check for prompt patterns (need at least one)
        has_pattern = any(pattern.lower() in content_lower 
                         for pattern in self.prompt_patterns)
        
        # For testing purposes, also accept simple keyword matches
        has_keywords = any(keyword.lower() in content_lower 
                         for keyword in self.keywords)
        
        if has_keywords:
            found_keywords = [keyword.lower() for keyword in self.keywords 
                            if keyword.lower() in content_lower]
            print(f"Found keywords: {found_keywords}")
            
        # Accept if it has either (required keywords + pattern) OR multiple keywords
        return (has_required and has_pattern) or (has_keywords and len(found_keywords) > 1)

    def _extract_prompt(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract actual jailbreak prompts from content
        """
        prompts = []
        lines = content.split('\n')
        current_prompt = []
        in_prompt = False
        
        for line in lines:
            # Check if line contains a prompt pattern
            if any(pattern.lower() in line.lower() for pattern in self.prompt_patterns):
                if current_prompt:  # Save previous prompt if exists
                    prompts.append(self._process_prompt(''.join(current_prompt)))
                current_prompt = [line]
                in_prompt = True
                continue
            
            # End of prompt markers
            if in_prompt and (line.strip() == '' or '[END]' in line or 'Assistant:' in line):
                if current_prompt:
                    prompts.append(self._process_prompt(''.join(current_prompt)))
                current_prompt = []
                in_prompt = False
                continue
                
            if in_prompt:
                current_prompt.append(line)
        
        # Don't forget last prompt if exists
        if current_prompt:
            prompts.append(self._process_prompt(''.join(current_prompt)))
            
        return prompts

    def _process_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """
        Process a single prompt to identify its type and target
        """
        prompt_type = "unknown"
        for type_name, patterns in self.jailbreak_types.items():
            if any(pattern.lower() in prompt_text.lower() for pattern in patterns):
                prompt_type = type_name
                break
                
        return {
            "prompt_text": prompt_text.strip(),
            "type": prompt_type,
            "length": len(prompt_text),
            "has_formatting": any(pattern in prompt_text for pattern in ["###", "<|", "=/"])
        }

    def _collect_from_repo(self, repo_name: str, branch: str) -> List[Dict[str, Any]]:
        """Optimized collection focusing only on relevant files"""
        collected_prompts = []
        
        try:
            print(f"\nSearching in {repo_name}...")
            repo = self.github.get_repo(repo_name)
            
            # Only look in specific paths
            target_paths = ["prompts", "jailbreak", "examples", "README.md"]
            
            for path in target_paths:
                try:
                    files = repo.get_contents(path, ref=branch)
                    if not isinstance(files, list):
                        files = [files]
                    
                    for file in files:
                        if file.name.endswith(('.md', '.txt')):
                            self._process_file(file, repo, collected_prompts)
                except:
                    continue  # Skip if path doesn't exist
                    
        except Exception as e:
            print(f"Error processing repository {repo_name}: {str(e)}")
            
        return collected_prompts

    def _process_file(self, file, repo, collected_prompts):
        """Simplified file processing"""
        content = self._extract_content(file)
        if not content or not self._contains_relevant_content(content):
            return
            
        prompts = self._extract_prompt(content)
        if prompts:
            for prompt in prompts:
                prompt_data = {
                    "source": {
                        "repo": repo.full_name,
                        "file": file.path,
                        "url": file.html_url
                    },
                    **prompt
                }
                collected_prompts.append(prompt_data)
                print(f"Found prompt in {file.path}")

    def search_additional_repos(self) -> List[tuple]:
        """Search GitHub for additional repositories with jailbreak content"""
        found_repos = set()
        
        print("\nSearching for additional repositories...")
        for search_term in self.search_terms:
            try:
                # Search in code content
                print(f"Searching for: {search_term}")
                code_results = self.github.search_code(
                    query=search_term,
                    sort='indexed',
                    order='desc'
                ).get_page(0)  # Get first page of results safely
                
                # Add repositories that contain matching code
                if code_results:  # Check if we have results
                    for result in code_results:
                        repo = result.repository
                        if repo.full_name not in [r[0] for r in self.primary_repos]:
                            found_repos.add((repo.full_name, repo.default_branch))
                            print(f"Found new repository: {repo.full_name}")
                else:
                    print(f"No results found for: {search_term}")
                
            except Exception as e:
                print(f"Error during search: {str(e)}")
                continue
                
        return list(found_repos)

    def collect(self) -> List[Dict[str, Any]]:
        """Collect prompts from both known repos and GitHub search"""
        collected_prompts = []
        
        # First check known repositories
        print("\nChecking known high-value repositories...")
        for repo_name, branch in self.primary_repos:
            try:
                prompts = self._collect_from_repo(repo_name, branch)
                if prompts:
                    collected_prompts.extend(prompts)
                    print(f"Found {len(prompts)} prompts in {repo_name}")
            except Exception as e:
                print(f"Error processing {repo_name}: {str(e)}")
                continue

        # Then search for additional repositories
        print("\nSearching for additional repositories...")
        additional_repos = self.search_additional_repos()
        print(f"\nFound {len(additional_repos)} additional repositories to check")
        
        for repo_name, branch in additional_repos:
            try:
                prompts = self._collect_from_repo(repo_name, branch)
                if prompts:
                    collected_prompts.extend(prompts)
                    print(f"Found {len(prompts)} prompts in {repo_name}")
            except Exception as e:
                print(f"Error processing {repo_name}: {str(e)}")
                continue

        print(f"\nTotal prompts collected: {len(collected_prompts)}")
        return collected_prompts 