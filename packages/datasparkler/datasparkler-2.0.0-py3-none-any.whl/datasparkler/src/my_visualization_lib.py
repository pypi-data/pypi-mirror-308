import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, data):
        """Initialize the DataVisualizer with data. 
    
        Args:
            data (list): The data to visualize.
        """
        self.data = data

    def visualize_data(self, x_key, y_key=None, plot_type='scatter'):
        """Visualize data using Matplotlib.
        
        Args:
            x_key (str): The key for the x-axis values.
            y_key (str, optional): The key for the y-axis values.
            plot_type (str): The type of plot to create.
        """
        # Prepare x and y values
        x_values = [entry[x_key] for entry in self.data if x_key in entry]
        
        if y_key:
            y_values = [entry[y_key] for entry in self.data if y_key in entry]

        plt.figure(figsize=(10, 6))

        # Create the specified type of plot
        if plot_type == 'scatter':
            plt.scatter(x_values, y_values, color='blue')
            plt.title(f'Scatter Plot of {y_key} vs {x_key}')
            plt.xlabel(x_key)
            plt.ylabel(y_key)
        elif plot_type == 'histogram':
            plt.hist(x_values, bins=10, color='green', alpha=0.7)
            plt.title(f'Histogram of {x_key}')
            plt.xlabel(x_key)
            plt.ylabel('Frequency')
        elif plot_type == 'pie':
            plt.pie(x_values, labels=[str(i) for i in range(len(x_values))], autopct='%1.1f%%')
            plt.title('Pie Chart')