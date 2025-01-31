import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib.gridspec as gridspec

# Define figure with GridSpec for fine-tuned subplot alignment
fig = plt.figure(figsize=(14, 6))
gs = gridspec.GridSpec(2, 14)  # More columns to allow precise alignment

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

# Assign plots dynamically based on total count
for i, category in enumerate(categories):
    if i < num_top:
        ax = plt.subplot(gs[0, 2 * i:2 * i + 2])  # Top row, evenly spaced
    else:
        ax = plt.subplot(gs[1, 2 * (i - num_top) + 1:2 * (i - num_top) + 3])  # Bottom row, centered

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
        x[-1], y.max() * 1.1, f"{latest_value}", 
        fontsize=16, fontweight="bold", color=plot_color, ha="right"
    )

    # Set category name next to the latest value
    ax.text(
        x[-1], y.max() * 0.9, category, fontsize=10, fontweight="bold", ha="right"
    )

    # Set month initials as x-axis labels but REMOVE the tick marks
    ax.set_xticks(x)  # Set ticks to align labels properly
    ax.set_xticklabels(month_letters, fontsize=9)
    ax.tick_params(axis='x', length=0)  # ✅ Hide tick marks

    # Hide grid and unnecessary spines
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Remove y-axis labels and ticks
    ax.set_yticks([])
    ax.set_ylabel("")

# Adjust spacing for a clean layout
plt.subplots_adjust(wspace=0.4, hspace=0.6)
plt.suptitle("Incident Category Trends", fontsize=14, fontweight="bold")

# Show plot
plt.show()
