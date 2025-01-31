import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

# Define the number of rows and columns for the subplot layout
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(14, 6))

# Flatten axes for easier indexing
axes = axes.flatten()

# Define smoothing method (choose between Moving Average or Spline)
def smooth_series(x, y):
    if len(x) > 3:  # Ensure enough points for smoothing
        spline = make_interp_spline(x, y, k=3)  # k=3 for cubic spline
        x_smooth = np.linspace(x.min(), x.max(), 300)
        y_smooth = spline(x_smooth)
    else:
        x_smooth, y_smooth = x, y  # No smoothing if too few points
    return x_smooth, y_smooth

# Set consistent colors
plot_color = "#144D9A"

# Get the column names (categories) and ensure correct subplot positions
categories = result_freq.columns

# Define position mapping for 3-top, 4-bottom layout
subplot_positions = [0, 1, 2, 4, 5, 6, 7]  # Skip index 3 to create a gap

for i, (category, subplot_index) in enumerate(zip(categories, subplot_positions)):
    ax = axes[subplot_index]  # Use mapped positions

    # Data points
    x = np.arange(len(result_freq.index))
    y = result_freq[category].values

    # Smooth the curve
    x_smooth, y_smooth = smooth_series(x, y)

    # Plot
    ax.plot(x_smooth, y_smooth, color=plot_color, linewidth=2)

    # Display the latest value in bold
    latest_value = result_freq[category].iloc[-1]
    ax.text(
        x[0], y.max() * 1.1, f"{latest_value}", 
        fontsize=16, fontweight="bold", color=plot_color, ha="left"
    )

    # Set category name below the number
    ax.text(
        x[0], y.max() * 0.9, category, fontsize=10, fontweight="bold", ha="left"
    )

    # Hide grid and unnecessary spines
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Remove ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

# Hide the unused 4th subplot in the top row
axes[3].axis("off")

# Adjust spacing
plt.subplots_adjust(wspace=0.4, hspace=0.6)
plt.suptitle("Incident Category Trends", fontsize=14, fontweight="bold")

# Show plot
plt.show()
