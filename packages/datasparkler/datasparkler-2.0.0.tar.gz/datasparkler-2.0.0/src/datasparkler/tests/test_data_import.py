# tests/test_data_import.py

import unittest
import sys
sys.path.append('e:\\ACADEMIA\\ACADEMIA\\SEM 1 YEAR 4\\MINI PROJECT\\DataPreprocessingLibrary\\src')

from my_data_import_lib import DataImporter

class TestDataImporter(unittest.TestCase):
    def test_from_csv(self):
        """Test importing data from a CSV file."""
        data = DataImporter.from_csv('data/sample_data.csv')
        self.assertIsInstance(data, list)  # Check if the result is a list
        self.assertGreater(len(data), 0)   # Ensure data is not empty

    def test_from_json(self):
        """Test importing data from a JSON file."""
        data = DataImporter.from_json('data/sample_data.json')
        self.assertIsInstance(data, list)  # Check if the result is a list
        self.assertGreater(len(data), 0)   # Ensure data is not empty

    def test_from_excel(self):
        """Test importing data from an Excel file."""
        data = DataImporter.from_excel('data/sample_data.xlsx')
        self.assertIsInstance(data, list)  # Check if the result is a list
        self.assertGreater(len(data), 0)   # Ensure data is not empty

if __name__ == '__main__':
    unittest.main()