import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

# Example DataFrame (replace with your actual data)
data = {
    'Event Time': [
        '2024-12-01 08:30:00', '2024-12-01 09:00:00', '2024-12-01 10:15:00',
        '2024-12-02 08:45:00', '2024-12-02 09:20:00', '2024-12-03 11:00:00',
        '2024-12-03 11:30:00', '2024-12-04 12:00:00', '2024-12-05 13:15:00'
    ]
}
df = pd.DataFrame(data)

# Convert "Event Time" to datetime
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Aggregate event counts by day
df['Date'] = df['Event Time'].dt.date
daily_counts = df.groupby('Date').size()

# Create a time series with a DatetimeIndex
time_series = pd.Series(daily_counts.values, index=pd.to_datetime(daily_counts.index))

# Perform seasonal decomposition using STL
stl = STL(time_series, seasonal=7)  # Adjust `seasonal` to match your data's frequency
result = stl.fit()

# Plot the decomposition
result.plot()
plt.suptitle("Seasonal Decomposition of Event Counts", fontsize=16)
plt.show()
