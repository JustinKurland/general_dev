# Ensure all series have a proper DatetimeIndex
minute_counts_series.index = pd.to_datetime(minute_counts_series.index)
hourly_counts_series.index = pd.to_datetime(hourly_counts_series.index)
daily_counts_series.index = pd.to_datetime(daily_counts_series.index)

# Resample and aggregate data to desired frequencies
aligned_minute = minute_counts_series.resample('H').sum()  # Aggregate minute data into hourly bins
aligned_hourly_again = hourly_counts_series.resample('H').mean()  # Ensure consistent hourly bins
aligned_daily = daily_counts_series.resample('D').sum()  # Aggregate daily data into daily bins

# Align all series to a common index
# Union of indices to ensure all timestamps are covered
common_index = aligned_minute.index.union(aligned_hourly_again.index).union(aligned_daily.index)

# Reindex each series to the common index and fill missing values with 0
aligned_minute = aligned_minute.reindex(common_index).fillna(0)
aligned_hourly_again = aligned_hourly_again.reindex(common_index).fillna(0)
aligned_daily = aligned_daily.reindex(common_index).fillna(0)

# Debugging: Check the lengths and data of aligned series
print(f"Aligned Minute Series:\n{aligned_minute.head(10)}")
print(f"Aligned Hourly Series:\n{aligned_hourly_again.head(10)}")
print(f"Aligned Daily Series:\n{aligned_daily.head(10)}")


from scipy.fftpack import fft
import numpy as np

# Compute Fourier Transform for each series
fft_minute = np.abs(fft(aligned_minute - aligned_minute.mean()))
fft_hourly = np.abs(fft(aligned_hourly_again - aligned_hourly_again.mean()))
fft_daily = np.abs(fft(aligned_daily - aligned_daily.mean()))

# Plot FFT results
plt.figure(figsize=(12, 6))
plt.plot(fft_minute[:len(fft_minute)//2], label="Minute-Level FFT")
plt.plot(fft_hourly[:len(fft_hourly)//2], label="Hourly-Level FFT")
plt.plot(fft_daily[:len(fft_daily)//2], label="Daily-Level FFT")
plt.title("Frequency Domain Analysis")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.legend()
plt.show()



from scipy.fftpack import fft
import numpy as np

# Compute Fourier Transform for each series
fft_minute = np.abs(fft(aligned_minute - aligned_minute.mean()))
fft_hourly = np.abs(fft(aligned_hourly_again - aligned_hourly_again.mean()))
fft_daily = np.abs(fft(aligned_daily - aligned_daily.mean()))

# Plot FFT results
plt.figure(figsize=(12, 6))
plt.plot(fft_minute[:len(fft_minute)//2], label="Minute-Level FFT")
plt.plot(fft_hourly[:len(fft_hourly)//2], label="Hourly-Level FFT")
plt.plot(fft_daily[:len(fft_daily)//2], label="Daily-Level FFT")
plt.title("Frequency Domain Analysis")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.legend()
plt.show()


import seaborn as sns

# Example: Create a heatmap for hourly data
hourly_heatmap = aligned_hourly_again.groupby([aligned_hourly_again.index.date, aligned_hourly_again.index.hour]).sum().unstack()

plt.figure(figsize=(12, 8))
sns.heatmap(hourly_heatmap, cmap="coolwarm", cbar=True)
plt.title("Hourly Activity Heatmap")
plt.xlabel("Hour of Day")
plt.ylabel("Date")
plt.show()
