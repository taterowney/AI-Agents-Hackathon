import unittest
from collectors.google_collector import GoogleCollector
import json
from datetime import datetime
import os
from dotenv import load_dotenv

class TestGoogleCollector(unittest.TestCase):
    def setUp(self):
        # Find and load the .env file from the parent directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)  # Go up one level to jailbreak-detector/
        dotenv_path = os.path.join(root_dir, '.env')
        
        # Load environment variables
        load_dotenv(dotenv_path)
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            self.skipTest("ANTHROPIC_API_KEY not found in environment variables")
            
        self.collector = GoogleCollector()
    
    def test_real_collection(self):
        """Test actual collection from Google"""
        print("\nTesting Google collection...")
        results = self.collector.collect()
        
        self.assertIsInstance(results, list)
        print(f"\nFound {len(results)} prompts")
        
        if results:
            # Save results
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_dir = os.path.join(project_root, "data", "raw")
            os.makedirs(data_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = os.path.join(data_dir, f"google_results_{timestamp}.json")
            
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\nResults saved to: {results_file}") 