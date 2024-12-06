# my_data_saving_lib.py

import json
import os

class DataSaver:
    def __init__(self, save_file):
        """Initialize the DataSaver with the path to the save file."""
        self.save_file = save_file

    def save_data(self, data):
        """Save the current state of the data to a JSON file.
        
        Args:
            data (list or dict): The data to be saved.
        """
        with open(self.save_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_data(self):
        """Load the data from the save file if it exists.
        
        Returns:
            list or dict: The loaded data, or None if the save file does not exist.
        """
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None