import unittest
from collectors.arxiv_collector import ArxivCollector
import json
from datetime import datetime
import os
from dotenv import load_dotenv

class TestArxivCollector(unittest.TestCase):
    def setUp(self):
        # Find the root directory and load .env from there
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)  # Go up one level to jailbreak-detector/
        dotenv_path = os.path.join(root_dir, '.env')
        
        # Load environment variables from the correct path
        load_dotenv(dotenv_path)
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            self.skipTest("ANTHROPIC_API_KEY not found in environment variables")
        self.collector = ArxivCollector()
    
    def test_real_collection(self):
        """Test actual collection from ArXiv"""
        print("\nTesting ArXiv collection...")
        results = self.collector.collect()
        
        self.assertIsInstance(results, list)
        print(f"\nFound {len(results)} papers")
        
        if results:
            # Save results
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_dir = os.path.join(project_root, "data", "raw")
            os.makedirs(data_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = os.path.join(data_dir, f"arxiv_results_{timestamp}.json")
            
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\nResults saved to: {results_file}")
            
            # Print first result with prompts
            first_paper = results[0]
            print("\nSample paper:")
            print(f"Title: {first_paper['title']}")
            print(f"Authors: {', '.join(first_paper['authors'])}")
            print(f"Keywords: {', '.join(first_paper['keywords_found'])}")
            
            if first_paper['prompts']:
                print("\nExample prompts found:")
                for i, prompt in enumerate(first_paper['prompts'][:3], 1):
                    print(f"\nPrompt {i}:")
                    print(prompt['text'][:200] + "..." if len(prompt['text']) > 200 else prompt['text'])

if __name__ == '__main__':
    unittest.main() 