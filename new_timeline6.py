import pandas as pd
import matplotlib.pyplot as plt

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

# Create the plot
customers = df["customer"].unique()
fig, axes = plt.subplots(len(customers), 1, figsize=(12, 6 * len(customers)), sharex=True)

if len(customers) == 1:  # If there's only one customer, `axes` won't be an array
    axes = [axes]

for ax, customer in zip(axes, customers):
    customer_data = df[df["customer"] == customer]

    # Extract time for plotting
    times = customer_data["_time"]
    prev_time = None

    # Plot each point
    for idx, row in customer_data.iterrows():
        # Plot the point on the timeline
        ax.plot(row["_time"], 0, 'o', markersize=8, label=f"{customer}'s Events", color='blue')

        # Calculate time delta
        time_delta = f"{(row['_time'] - prev_time)}" if prev_time is not None else "N/A"
        prev_time = row["_time"]

        # Add a text box with details
        text = (
            f"IP: {row['IP']}\n"
            f"Action: {row['action']}\n"
            f"Device: {row['device']}\n"
            f"Time Delta: {time_delta}"
        )
        ax.text(
            row["_time"],
            0.1,  # Position the text slightly above the point
            text,
            fontsize=10,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
        )

    # Set titles and remove y-axis
    ax.set_title(f"Timeline of Events for Customer: {customer}", fontsize=14)
    ax.get_yaxis().set_visible(False)
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)

    # Format the x-axis to show full datetime with microseconds and timezone
    def format_datetime(x, _):
        return pd.Timestamp(x).strftime("%Y-%m-%d %H:%M:%S.%f%z")

    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_datetime))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")  # Rotate labels for readability

# Shared X-axis label
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Time", fontsize=14)
plt.tight_layout()
plt.show()
