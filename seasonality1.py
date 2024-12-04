import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

# Example DataFrame (replace with your actual data)
data = {
    'Event Time': [
        '2024-12-01 08:30:00', '2024-12-01 08:35:00', '2024-12-01 09:00:00',
        '2024-12-01 09:15:00', '2024-12-01 10:00:00', '2024-12-02 10:30:00',
        '2024-12-02 11:00:00', '2024-12-02 12:00:00', '2024-12-03 12:30:00'
    ]
}
df = pd.DataFrame(data)
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Define temporal units for analysis
temporal_units = {'T': 'Minutes', 'H': 'Hours', 'D': 'Days'}
results = {}

for unit, label in temporal_units.items():
    print(f"\nProcessing {label}-Level Data...\n")

    # Resample data at the specified temporal level
    resampled = df.set_index('Event Time').resample(unit).size()

    # Handle missing values (fill gaps with 0 for continuous time series)
    resampled = resampled.asfreq(unit, fill_value=0)

    # Explicitly set the frequency
    resampled.index.freq = unit

    # Set seasonal period based on unit
    seasonal_period = 7 if unit == 'D' else (24 if unit == 'H' else 60)

    # Perform STL decomposition
    try:
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

    except Exception as e:
        print(f"STL Decomposition failed for {label} due to: {e}")
        results[label] = {'Seasonality Strength': 'N/A'}

# Summarize results across temporal levels
results_df = pd.DataFrame(results).T
results_df.index.name = "Temporal Unit"
results_df.reset_index(inplace=True)

import ace_tools as tools; tools.display_dataframe_to_user(name="Temporal Unit Analysis Results", dataframe=results_df)
