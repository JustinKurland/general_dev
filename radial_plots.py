import matplotlib.pyplot as plt
import numpy as np

# Define the correct month order with January always at 12 o’clock position
month_labels = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

# Define the provided data again
data_values = {
    "RL1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "RL2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "RL3": [32, 35, 38, 39, 6, 7, 8, 7, 11, 8, 2, 4],
    "RL4": [0, 4, 3, 10, 53, 76, 79, 141, 135, 120, 108, 92],
}

# Define the colors for each group
colors = ["#3B7CDE", "#7297c5", "#A6428c", "#159788"]

# Convert months to angles for radial plot, ensuring January is at the top (12 o’clock position)
angles = np.linspace(0, 2 * np.pi, len(month_labels), endpoint=False).tolist()

# Ensure circular continuity by appending the first value to close the loop
angles.append(angles[0])

# Create Subplots (Radial) with the given data
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10), subplot_kw=dict(polar=True))
axes = axes.flatten()

# Set a consistent scale across all plots
max_value = max(max(values) for values in data_values.values())
y_ticks = np.linspace(0, max_value, 5, dtype=int)  # Convert y-ticks to integers

# Plot each group in its respective subplot
for i, (group, values) in enumerate(data_values.items()):
    shifted_values = values[:] + [values[0]]  # Close the circular plot properly

    axes[i].set_theta_zero_location("N")  # Set January (top) at 12 o'clock
    axes[i].set_theta_direction(-1)  # Make the radial plot go clockwise

    axes[i].plot(angles, shifted_values, marker="o", linestyle="-", label=group, color=colors[i])
    axes[i].fill(angles, shifted_values, alpha=0.3, color=colors[i])  # Fill area under the curve
    axes[i].set_title(group)
    axes[i].set_xticks(angles[:-1])
    axes[i].set_xticklabels(month_labels)  # Keep the month labels exactly as shown

    # Keep y-scale consistent across plots and set integer y-ticks
    axes[i].set_yticks(y_ticks)
    axes[i].set_yticklabels([str(y) for y in y_ticks])  # Convert y-tick labels to integers

# Adjust layout
plt.tight_layout()
plt.show()
