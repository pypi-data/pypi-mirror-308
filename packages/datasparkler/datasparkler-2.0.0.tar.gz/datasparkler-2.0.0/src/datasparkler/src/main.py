# main.py

from my_data_import_lib import DataImporter
from my_data_preprocessing_lib import DataPreprocessor
from my_data_saving_lib import DataSaver
from my_visualization_lib import DataVisualizer

def main():
    # Step 1: Import data from a CSV file
    print("Importing data from CSV...")
    data = DataImporter.from_csv('data/sample_data.csv')
    
    # Step 2: Initialize DataSaver to save processed data
    data_saver = DataSaver('data/processed_data.json')
    
    # Step 3: Initialize DataPreprocessor with the imported data
    preprocessor = DataPreprocessor(data, data_saver)
    
    # Step 4: Clean the data
    print("Cleaning data...")
    cleaned_data = preprocessor.clean_data()
    
    # Step 5: Normalize the data
    print("Normalizing data...")
    normalized_data = preprocessor.normalize_data(method='minmax')
    
    # Step 6: Feature engineering (example: creating a new feature)
    print("Creating new feature...")
    def new_feature(entry):
        return entry['A'] * 2  # Example feature: double the value of A
    
    preprocessor.feature_engineering('D', new_feature)
    
    # Step 7: Visualize the data
    print("Visualizing data...")
    visualizer = DataVisualizer(normalized_data)
    visualizer.visualize_data('A', 'C', plot_type='scatter')
    
    # Optional: Save the processed data
    print("Saving processed data...")
    data_saver.save_data(normalized_data)

    print("Data processing complete!")

if __name__ == '__main__':
    main()