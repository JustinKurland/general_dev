import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame (replace this with your actual DataFrame)
data = {
    'Event Time': [
        '2024-12-01 08:30:00', '2024-12-01 09:00:00', '2024-12-01 10:15:00',
        '2024-12-02 08:45:00', '2024-12-02 09:20:00', '2024-12-03 11:00:00'
    ]
}
df = pd.DataFrame(data)

# Convert "Event Time" to datetime
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Add a Date column for aggregation
df['Date'] = df['Event Time'].dt.date

# Group by date and count events
daily_counts = df.groupby('Date').size()

# Plot daily trends
plt.figure(figsize=(10, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')
plt.title("Event Counts Over Time", fontsize=16)
plt.xlabel("Date", fontsize=14)
plt.ylabel("Number of Events", fontsize=14)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
