import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib.gridspec as gridspec

# Define figure with adjusted aspect ratio and proper spacing
fig = plt.figure(figsize=(16, 6))
gs = gridspec.GridSpec(2, 14, height_ratios=[0.5, 0.5], hspace=0.8)

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

    # Set individual max value for each y-axis based on its own data
    max_y_value = max(y) * 1.2  # Scale slightly higher for better visibility
    y_tick_values = np.linspace(0, max_y_value, num=3, dtype=int)  # Dynamic y-ticks per plot

    # Adjust text placement dynamically to avoid overlap with the lines
    latest_value = result_freq[category].iloc[-1]
    y_text_position = max_y_value * 1.05 if latest_value < max_y_value * 0.8 else max_y_value * 0.2  # Adjust dynamically

    # Display the latest value in bold
    ax.text(
        x[-1], y_text_position, f"{latest_value}", 
        fontsize=14, fontweight="bold", color=plot_color, ha="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.8)
    )

    # Adjust category title placement based on max value to avoid overlap
    title_y_position = max_y_value * 1.15 if max(y) < max_y_value * 0.8 else max_y_value * 0.3

    # Set category name above the plot, centered, avoiding overlaps
    ax.text(
        x[len(x) // 2], title_y_position, category, fontsize=12, fontweight="bold", ha="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.8)
    )

    # Set month initials as x-axis labels but REMOVE the tick marks
    ax.set_xticks(x)  # Set ticks to align labels properly
    ax.set_xticklabels(month_letters, fontsize=10)
    ax.tick_params(axis='x', length=0)  # Hide tick marks

    # Set individual y-axis tick labels
    ax.set_yticks(y_tick_values)
    ax.set_yticklabels([str(val) for val in y_tick_values], fontsize=8)

    # Set dynamic y-axis limits
    ax.set_ylim(0, max_y_value)

    # Hide grid and unnecessary spines
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

# Adjust spacing for a clean layout
plt.subplots_adjust(wspace=0.6, hspace=1.0)
plt.suptitle("Incident Category Trends", fontsize=16, fontweight="bold")

# Show plot
plt.show()
