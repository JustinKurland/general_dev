import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colorbar as cbar
from matplotlib.colors import LinearSegmentedColormap

# Define the colormap (same as in the DataFrame)
colors = ['#ffffff', '#2f3b5c']
n_bins = 100  # Number of gradient levels
cmap_name = 'custom_cmap'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 1))  # Adjust size to fit well
fig.subplots_adjust(bottom=0.5)

# Create a color bar
cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=custom_cmap), cax=ax, orientation='horizontal')

# Label the color bar (adjust min/max values to match the table)
cbar.set_label('Gradient Scale (Min → Max Values)', fontsize=12)

# Show the color scale
plt.show()
