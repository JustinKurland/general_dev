# Resample the data
resampled = df.resample(unit).size()

# Explicitly set the frequency for the resampled series
if unit == 'T':
    resampled.index.freq = 'T'  # Ensure 'T' for minutes
elif unit == 'H':
    resampled.index.freq = 'H'  # Ensure 'H' for hours
elif unit == 'D':
    resampled.index.freq = 'D'  # Ensure 'D' for days

# Perform STL decomposition
seasonal_period = 7 if unit == 'D' else (24 if unit == 'H' else 60)  # Seasonal period
stl = STL(resampled, seasonal=seasonal_period).fit()

# Plot the decomposition
stl.plot()
plt.suptitle(f"STL Decomposition ({label})", fontsize=16)
plt.show()
