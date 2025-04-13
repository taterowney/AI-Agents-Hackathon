import json
from datetime import datetime
from typing import Dict, Any
import os

class DataProcessor:
    def __init__(self):
        self.raw_data_dir = "data/raw"
        self.processed_data_dir = "data/processed"
        
        # Create directories if they don't exist
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
    
    def save_raw_data(self, data: Dict[str, Any], source: str):
        """
        Saves raw data with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source}_{timestamp}.json"
        
        filepath = os.path.join(self.raw_data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2) 