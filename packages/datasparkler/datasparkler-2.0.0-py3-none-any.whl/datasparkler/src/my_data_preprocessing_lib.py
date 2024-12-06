# my_data_preprocessing_lib.py

class DataPreprocessor:
    def __init__(self, data, data_saver):
        """Initialize the DataPreprocessor with data and a DataSaver instance.
        
        Args:
            data (list): The initial data to process.
            data_saver (DataSaver): An instance of DataSaver for saving the data.
        """
        if not self.is_valid_data(data):
            raise ValueError("Input data must be a 2D array (list of lists) or a list of dictionaries.")
        self.data = data
        self.data_saver = data_saver

    def is_valid_data(self, data):
        """Check if the data is a valid 2D structure.
        
        Args:
            data (any): The data to validate.
        
        Returns:
            bool: True if the data is valid; False otherwise.
        """
        if isinstance(data, list):
            if len(data) == 0:
                return False
            if isinstance(data[0], dict):
                return True  # List of dictionaries
            elif isinstance(data[0], list):
                return all(isinstance(row, list) for row in data)  # List of lists
        return False

    def clean_data(self):
        """Remove entries with missing values and duplicates.
        
        Returns:
            list: The cleaned data.
        """
        seen = set()
        cleaned_data = []
        
        for entry in self.data:
            entry_tuple = tuple(entry.items()) if isinstance(entry, dict) else tuple(entry)
            if entry_tuple not in seen and all(value is not None for value in entry.values() if isinstance(entry, dict)):
                seen.add(entry_tuple)
                cleaned_data.append(entry)
        
        self.data = cleaned_data
        # Save the cleaned data
        self.data_saver.save_data(self.data)
        return self.data

    def normalize_data(self, method='minmax'):
        """Normalize the data using the specified method ('minmax' or 'standard').
        
        Args:
            method (str): The normalization method to use.
        
        Returns:
            list: The normalized data.
        """
        if not self.data:
            return []

        # Create a dictionary to hold numeric columns
        numeric_columns = {key: [] for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))} if isinstance(self.data[0], dict) else {}
        
        # Collect values for normalization
        for entry in self.data:
            for key in numeric_columns.keys() if isinstance(entry, dict) else range(len(entry)):
                value = entry[key] if isinstance(entry, dict) else entry[key]
                numeric_columns[key].append(value)

        normalized_data = []
        
        # Normalize each entry
        for entry in self.data:
            normalized_entry = entry.copy() if isinstance(entry, dict) else entry[:]
            for key in numeric_columns.keys() if isinstance(entry, dict) else range(len(entry)):
                if method == 'minmax':
                    min_val = min(numeric_columns[key])
                    max_val = max(numeric_columns[key])
                    normalized_value = (entry[key] - min_val) / (max_val - min_val) if max_val - min_val != 0 else 0
                elif method == 'standard':
                    mean_val = sum(numeric_columns[key]) / len(numeric_columns[key])
                    std_val = (sum((x - mean_val) ** 2 for x in numeric_columns[key]) / len(numeric_columns[key])) ** 0.5
                    normalized_value = (entry[key] - mean_val) / std_val if std_val != 0 else 0
                else:
                    raise ValueError("Method must be 'minmax' or 'standard'")
                
                if isinstance(normalized_entry, dict):
                    normalized_entry[key] = normalized_value
                else:
                    normalized_entry[key] = normalized_value
            
            normalized_data.append(normalized_entry)

        self.data = normalized_data
        # Save the normalized data
        self.data_saver.save_data(self.data)
        return self.data

    def feature_engineering(self, new_feature_name, func):
        """Create a new feature from existing features.
        
        Args:
            new_feature_name (str): The name of the new feature to add.
            func (callable): A function that computes the new feature.
        
        Returns:
            list: The data with the new feature added.
        """
        for entry in self.data:
            entry[new_feature_name] = func(entry)
        # Save after feature engineering
        self.data_saver.save_data(self.data)
        return self.data

    def validate_data(self, validation_rules):
        """Validate data against given rules.
        
        Args:
            validation_rules (list): A list of validation functions.
        
        Returns:
            bool: True if all validations pass; False otherwise.
        """
        for rule in validation_rules:
            if not rule(self.data):
                return False
        return True