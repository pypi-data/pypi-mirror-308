# my_data_import_lib.py

import csv
import json
import pandas as pd  # Optional, for reading Excel files

class DataImporter:
    @staticmethod
    def from_csv(file_path):
        """Read data from a CSV file and return a list of dictionaries.
        
        Args:
            file_path (str): The path to the CSV file.
        
        Returns:
            list: A list of dictionaries representing the rows in the CSV file.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    @staticmethod
    def from_json(file_path):
        """Read data from a JSON file and return a list of dictionaries.
        
        Args:
            file_path (str): The path to the JSON file.
        
        Returns:
            list: The loaded data as a list of dictionaries.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def from_excel(file_path, sheet_name=0):
        """Read data from an Excel file and return a list of dictionaries.
        
        Args:
            file_path (str): The path to the Excel file.
            sheet_name (int or str): The sheet name or index to read.
        
        Returns:
            list: A list of dictionaries representing the rows in the Excel sheet.
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.to_dict(orient='records')