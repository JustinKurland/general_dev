import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

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

# Extract times and events
dates = df["_time"]
events = [
    f"IP: {row['IP']}\nAction: {row['action']}\nDevice: {row['device']}"
    for _, row in df.iterrows()
]

# Stagger levels for the timeline
levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(df) / 6)))[: len(df)]

# Create the plot
fig, ax = plt.subplots(figsize=(12.8, 4), constrained_layout=True)
ax.set(title="Staggered Event Timeline")

# Plot the vertical stems
ax.vlines(dates, 0, levels, color="tab:red")
# Plot the baseline and markers
ax.plot(dates, np.zeros_like(dates), "-o", color="k", markerfacecolor="w")

# Annotate each event
for date, level, event in zip(dates, levels, events):
    ax.annotate(
        event,
        xy=(date, level),
        xytext=(-3, np.sign(level) * 3),
        textcoords="offset points",
        horizontalalignment="left",
        verticalalignment="bottom" if level > 0 else "top",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
        fontsize=9,
    )

# Format x-axis
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.Timestamp(x).strftime("%Y-%m-%d %H:%M:%S%z")))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# Clean up plot
ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.margins(y=0.1)

plt.show()
