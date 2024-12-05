import matplotlib.pyplot as plt
import pandas as pd

# Group data by day
daily_groups = hourly_counts_series.groupby(hourly_counts_series.index.date)

# Number of days in the series
num_days = len(daily_groups)

# Create a figure with subplots (adjust rows/columns as needed)
fig, axes = plt.subplots(nrows=num_days, ncols=1, figsize=(10, num_days * 3), sharex=True)

# If only one subplot, `axes` won't be an iterable, so wrap it in a list
if num_days == 1:
    axes = [axes]

# Loop through each day's data and plot
for ax, (day, group) in zip(axes, daily_groups):
    ax.plot(group.index, group.values, linestyle='-', marker='o', markersize=4)
    ax.set_title(f"Events on {day}", fontsize=12)
    ax.set_ylabel("Number of Events", fontsize=10)
    ax.grid(True)

# Adjust labels and spacing
axes[-1].set_xlabel("Time (Hour)", fontsize=12)  # Set xlabel only on the last subplot
plt.tight_layout()
plt.show()
