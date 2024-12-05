import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming `minute_counts_series`, `hourly_counts_series`, `daily_counts_series`, and `weekly_counts_series` are defined

# Step 1: Aggregate Patterns Across Temporal Units
# Align hourly and daily data by resampling to the same frequency
aligned_hourly = hourly_counts_series.resample('D').mean()  # Resample hourly data to daily frequency
aligned_daily = daily_counts_series.resample('D').mean()  # Resample daily data to daily frequency

# Align minute and hourly data
aligned_minute = minute_counts_series.resample('H').mean()  # Resample minute data to hourly frequency
aligned_hourly_again = hourly_counts_series.resample('H').mean()  # Ensure both are at hourly frequency

# Step 2: Compute Correlations
# Compute correlations between aligned data
correlation_hourly_daily = np.corrcoef(aligned_hourly, aligned_daily)[0, 1]
correlation_minute_hourly = np.corrcoef(aligned_minute, aligned_hourly_again)[0, 1]

# Print Correlations
print(f"Correlation between hourly and daily patterns: {correlation_hourly_daily:.2f}")
print(f"Correlation between minute and hourly patterns: {correlation_minute_hourly:.2f}")

# Step 3: Visualize Patterns
# Plot aligned hourly vs daily pattern
plt.figure(figsize=(10, 6))
plt.plot(aligned_hourly.index, aligned_hourly, label="Hourly Pattern")
plt.plot(aligned_daily.index, aligned_daily, label="Daily Pattern")
plt.title("Hourly vs Daily Patterns (Aligned)")
plt.xlabel("Date")
plt.ylabel("Average Activity")
plt.legend()
plt.show()

# Plot aligned minute vs hourly pattern
plt.figure(figsize=(10, 6))
plt.plot(aligned_minute.index, aligned_minute, label="Minute Pattern")
plt.plot(aligned_hourly_again.index, aligned_hourly_again, label="Hourly Pattern")
plt.title("Minute vs Hourly Patterns (Aligned)")
plt.xlabel("Date")
plt.ylabel("Average Activity")
plt.legend()
plt.show()
