import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Toy time series data with multiple columns
data = {
    'date': pd.date_range(start='2023-01-01', end='2023-06-01', freq='D'),
    'value1': np.random.randint(low=1, high=20, size=152),
    'value2': np.random.randint(low=1, high=20, size=152),
    'value3': np.random.randint(low=1, high=20, size=152)
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Set the 'date' column as the index
df.set_index('date', inplace=True)

# Resample the data based on the monthly unit and aggregate with a list of values
resampled_df = df.resample('M').agg(list)

# Get the list of column names except for 'date'
columns = resampled_df.columns[0:]

# Generate separate subplots for each column
num_plots = len(columns)
fig, axs = plt.subplots(num_plots, 1, figsize=(8, 5 * num_plots), sharex=True)

# Iterate over each column and create boxplots
for i, column in enumerate(columns):
    ax = axs[i]
    ax.boxplot(resampled_df[column])
    
    # Customize the plot for each column
    ax.set_ylabel(column)
    ax.set_title(f"Boxplots of {column}")
    
    # Set x-axis tick labels as month-year format for each subplot
    x_labels = resampled_df.index[:-1].strftime('%b-%Y')  # Exclude last index for first subplot
    ax.set_xticks(np.arange(1, len(resampled_df)))
    ax.set_xticklabels(x_labels, rotation=45)

# Display the plot
plt.tight_layout()
plt.show()
