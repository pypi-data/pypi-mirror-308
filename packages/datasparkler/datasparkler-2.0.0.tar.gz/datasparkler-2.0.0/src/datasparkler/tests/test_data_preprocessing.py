# tests/test_data_preprocessing.py

import unittest

import sys
sys.path.append('e:\\ACADEMIA\\ACADEMIA\\SEM 1 YEAR 4\\MINI PROJECT\\DataPreprocessingLibrary\\src')

from my_data_preprocessing_lib import DataPreprocessor
from my_data_saving_lib import DataSaver

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        """Set up a sample dataset and DataSaver for testing."""
        self.data = [
            {'A': 1, 'B': 'cat', 'C': 5},
            {'A': 2, 'B': 'dog', 'C': 6},
            {'A': None, 'B': 'cat', 'C': 7},
            {'A': 4, 'B': 'dog', 'C': 8},
            {'A': 2, 'B': 'dog', 'C': 6}  # Duplicate
        ]
        self.data_saver = DataSaver('data/test_saved_data.json')
        self.preprocessor = DataPreprocessor(self.data, self.data_saver)

    def test_clean_data(self):
        """Test the data cleaning functionality."""
        cleaned_data = self.preprocessor.clean_data()
        self.assertEqual(len(cleaned_data), 3)  # Should remove duplicates and None values
        print(cleaned_data)

    def test_normalize_data(self):
        """Test the normalization functionality."""
        self.preprocessor.clean_data()  # Clean data first
        normalized_data = self.preprocessor.normalize_data(method='minmax')
        self.assertTrue(all(0 <= entry['A'] <= 1 for entry in normalized_data))  # Check normalization
        

if __name__ == '__main__':
    unittest.main()