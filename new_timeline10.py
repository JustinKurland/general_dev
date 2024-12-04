import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Example DataFrame
data = {
    "_time": [
        "2024-12-04 10:59:18.639000-05:00",
        "2024-12-04 11:01:18.639000-05:00",
        "2024-12-04 11:30:18.639000-05:00",
        "2024-12-05 12:15:00.000000-05:00",
        "2024-12-06 12:30:00.000000-05:00",
    ],
    "customer": ["Alice", "Alice", "Alice", "Bob", "Bob"],
    "IP": ["192.168.1.1", "192.168.1.2", "192.168.1.1", "10.0.0.1", "10.0.0.2"],
    "device": ["laptop", "phone", "tablet", "laptop", "tablet"],
    "action": ["login", "browse", "logout", "login", "logout"],
}

df = pd.DataFrame(data)

# Convert _time to datetime
df["_time"] = pd.to_datetime(df["_time"])

# Sort by time for better visualization
df = df.sort_values(by=["customer", "_time"])

# Extract times and initialize levels
dates = df["_time"]

# Create a staggered sequence of levels for better visualization
level_pattern = [3, -3, 5, -5, 7, -7]  # Staggered levels
levels = np.tile(level_pattern, int(np.ceil(len(dates) / len(level_pattern))))[: len(dates)]

# The figure and axes
fig, ax = plt.subplots(figsize=(12, 6))
ax.set(title="Event Timeline")

# Plot the timeline
ax.vlines(dates, 0, levels, color="tab:blue")  # Stems
ax.scatter(dates, np.zeros_like(dates), color="black", zorder=3)  # Baseline markers
ax.axhline(0, color="black", linewidth=0.5)  # Baseline

# Annotate each event with a text box
for idx, (date, level) in enumerate(zip(dates, levels)):
    row = df.iloc[idx]
    text = (
        f"IP Address: {row['IP']}\n"
        f"Action: {row['action']}\n"
        f"Device: {row['device']}"
    )
    ax.annotate(
        text,
        xy=(date, level),
        xytext=(-3, np.sign(level) * 5),
        textcoords="offset points",
        verticalalignment="bottom" if level > 0 else "top",
        horizontalalignment="center",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
        fontsize=9,
    )

# Format the x-axis to show full datetime with timezone
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.Timestamp(x).strftime("%Y-%m-%d %H:%M:%S%z")))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Clean up the plot
ax.get_yaxis().set_visible(False)  # Hide y-axis
ax.spines[["left", "top", "right"]].set_visible(False)  # Hide unnecessary spines
ax.margins(y=0.1)

plt.show()
