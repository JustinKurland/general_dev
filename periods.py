# Set 'Event Time' as the index
df.set_index('Event Time', inplace=True)

# Resample by day and count the number of events
daily_counts = df.resample('D').size()

# Plot daily trends
plt.figure(figsize=(10, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')
plt.title("Daily Event Counts", fontsize=16)
plt.xlabel("Date", fontsize=14)
plt.ylabel("Number of Events", fontsize=14)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Resample at different temporal units
temporal_units = {'T': 'Minutes', 'H': 'Hours', 'D': 'Days'}
results = {}

for unit, label in temporal_units.items():
    # Resample data
    resampled = df.resample(unit).size()

    # Set frequency explicitly
    resampled.index.freq = pd.infer_freq(resampled.index)

    # Perform STL decomposition
    seasonal_period = 7 if unit == 'D' else (24 if unit == 'H' else 60)
    stl = STL(resampled, seasonal=seasonal_period).fit()

    # Plot decomposition
    stl.plot()
    plt.suptitle(f"STL Decomposition ({label})", fontsize=16)
    plt.show()

    # Compute seasonality strength
    seasonal_var = np.var(stl.seasonal)
    total_var = np.var(resampled)
    seasonality_strength = seasonal_var / total_var if total_var != 0 else 0

    # Store results
    results[label] = {'Seasonality Strength': seasonality_strength}

# Summarize results
results_df = pd.DataFrame(results).T
results_df.index.name = "Temporal Unit"
results_df.reset_index(inplace=True)

import ace_tools as tools; tools.display_dataframe_to_user(name="Temporal Unit Analysis Results", dataframe=results_df)
