import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib.gridspec as gridspec

# Define figure with more vertical space and adjusted GridSpec for better spacing
fig = plt.figure(figsize=(16, 8))  # Increased figure size
gs = gridspec.GridSpec(2, 14, height_ratios=[1, 1], hspace=0.8)  # Added more space between rows

# Define smoothing method (Spline Interpolation for smooth curves)
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

# Get the column names (categories)
categories = result_freq.columns

# Extract first letter of each month for x-axis labels (Aligned with DataFrame index)
month_letters = [m[0] for m in result_freq.index.strftime("%b")]

# Define custom GridSpec positions to properly align the rows
num_categories = len(categories)
num_top = (num_categories + 1) // 2  # Top row gets more plots if odd
num_bottom = num_categories - num_top

# Find a common y-axis limit that makes the plots shorter
global_max_value = max(result_freq.max()) * 1.2  # Set a consistent max limit across plots

# Assign plots dynamically based on total count
for i, category in enumerate(categories):
    if i < num_top:
        ax = plt.subplot(gs[0, 2 * i + 1:2 * i + 3])  # Top row, shifted slightly for balance
    else:
        ax = plt.subplot(gs[1, 2 * (i - num_top) + 2:2 * (i - num_top) + 4])  # Bottom row, centered

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
        x[-1], global_max_value * 0.95, f"{latest_value}", 
        fontsize=16, fontweight="bold", color=plot_color, ha="center"
    )

    # Set category name above the plot, centered
    ax.text(
        x[len(x) // 2], global_max_value * 1.05, category, fontsize=12, fontweight="bold", ha="center"
    )

    # Set month initials as x-axis labels but REMOVE the tick marks
    ax.set_xticks(x)  # Set ticks to align labels properly
    ax.set_xticklabels(month_letters, fontsize=10)
    ax.tick_params(axis='x', length=0)  # ✅ Hide tick marks

    # Set a fixed, lower y-axis limit to shorten the plots
    ax.set_ylim(0, global_max_value)

    # Hide grid and unnecessary spines
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Remove y-axis labels and ticks
    ax.set_yticks([])
    ax.set_ylabel("")

# Adjust spacing for a clean layout
plt.subplots_adjust(wspace=0.6, hspace=1.0)  # Increased spacing
plt.suptitle("Incident Category Trends", fontsize=16, fontweight="bold")

# Show plot
plt.show()
