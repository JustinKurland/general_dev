# Ensure both series have a DatetimeIndex
minute_counts_series.index = pd.to_datetime(minute_counts_series.index)
hourly_counts_series.index = pd.to_datetime(hourly_counts_series.index)

# Resample minute-level data to hourly
aligned_minute = minute_counts_series.resample('H').sum()  # Aggregate minute data into hourly frequency
aligned_hourly_again = hourly_counts_series.resample('H').mean()  # Ensure hourly data is consistent

# Align both series to a common index
common_index_minute_hourly = aligned_minute.index.intersection(aligned_hourly_again.index)

# Check for empty or missing data
print(f"Length of aligned_minute before alignment: {len(aligned_minute)}")
print(f"Length of aligned_hourly_again before alignment: {len(aligned_hourly_again)}")
print(f"Length of common_index_minute_hourly: {len(common_index_minute_hourly)}")

# Reindex both series to the common index and fill missing values
aligned_minute = aligned_minute.reindex(common_index_minute_hourly).fillna(0)
aligned_hourly_again = aligned_hourly_again.reindex(common_index_minute_hourly).fillna(0)

# Check for empty slices
print(f"Length of aligned_minute after alignment: {len(aligned_minute)}")
print(f"Length of aligned_hourly_again after alignment: {len(aligned_hourly_again)}")

# Ensure lengths match for correlation
if len(aligned_minute) != len(aligned_hourly_again):
    print("Error: Aligned series lengths do not match!")
else:
    # Compute Correlation
    correlation_minute_hourly = np.corrcoef(aligned_minute, aligned_hourly_again)[0, 1]
    print(f"Correlation between minute and hourly patterns: {correlation_minute_hourly:.2f}")

    # Visualize the aligned patterns
    plt.figure(figsize=(10, 6))
    plt.plot(aligned_minute.index, aligned_minute, label="Minute Pattern")
    plt.plot(aligned_hourly_again.index, aligned_hourly_again, label="Hourly Pattern")
    plt.title("Minute vs Hourly Patterns (Aligned)")
    plt.xlabel("Time")
    plt.ylabel("Average Activity")
    plt.legend()
    plt.show()
