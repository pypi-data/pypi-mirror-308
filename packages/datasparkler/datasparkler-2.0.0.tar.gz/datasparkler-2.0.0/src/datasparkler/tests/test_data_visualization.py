# tests/test_data_visualization.py

import unittest

import sys
sys.path.append('e:\\ACADEMIA\\ACADEMIA\\SEM 1 YEAR 4\\MINI PROJECT\\DataPreprocessingLibrary\\src')

from my_visualization_lib import DataVisualizer

class TestDataVisualizer(unittest.TestCase):
    def setUp(self):
        """Set up a sample dataset for testing visualization."""
        self.data = [
            {'A': 1, 'B': 'cat', 'C': 5},
            {'A': 2, 'B': 'dog', 'C': 6},
            {'A': 3, 'B': 'cat', 'C': 7},
            {'A': 4, 'B': 'dog', 'C': 8}
        ]
        self.visualizer = DataVisualizer(self.data)

    def test_visualize_data(self):
        """Test the visualization functionality (this will show plots)."""
        # Here we can test if the method runs without errors
        try:
            self.visualizer.visualize_data('A', 'C', plot_type='scatter')
            self.visualizer.visualize_data('A', plot_type='histogram')
            self.visualizer.visualize_data('A', plot_type='bar')
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()