import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import STL
from scipy.fftpack import fft
from pandas.plotting import autocorrelation_plot

# Example DataFrame (replace with your data)
data = {
    'Event Time': [
        '2024-12-01 08:30:15', '2024-12-01 08:30:45', '2024-12-01 08:31:15',
        '2024-12-01 09:00:15', '2024-12-01 09:01:15', '2024-12-02 10:15:15',
        '2024-12-02 10:16:15', '2024-12-02 11:00:15', '2024-12-03 12:15:15'
    ]
}
df = pd.DataFrame(data)

# Convert "Event Time" to datetime
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Define temporal units for aggregation
temporal_units = ['S', 'T', 'H', 'D']  # Seconds, Minutes, Hours, Days

results = {}

for unit in temporal_units:
    # Resample data
    resampled = df.set_index('Event Time').resample(unit).size()

    # Ensure time series has a DatetimeIndex
    time_series = pd.Series(resampled.values, index=resampled.index)

    # Decompose the time series
    stl = STL(time_series, seasonal=7 if unit in ['D'] else 24).fit()

    # Compute seasonality strength
    seasonal_var = np.var(stl.seasonal)
    total_var = np.var(time_series)
    seasonality_strength = seasonal_var / total_var if total_var != 0 else 0

    # Fourier Transform
    fft_result = fft(time_series - time_series.mean())
    frequencies = np.fft.fftfreq(len(fft_result))
    dominant_frequency = frequencies[np.argmax(np.abs(fft_result))]

    # Residual variance ratio
    residual_var = np.var(stl.resid)
    residual_to_total_ratio = residual_var / total_var if total_var != 0 else 0

    # Store results
    results[unit] = {
        'seasonality_strength': seasonality_strength,
        'dominant_frequency': dominant_frequency,
        'residual_to_total_ratio': residual_to_total_ratio
    }

    # Plot decomposition
    stl.plot()
    plt.suptitle(f"STL Decomposition at {unit} Level", fontsize=16)
    plt.show()

    # Autocorrelation
    print(f"Autocorrelation Plot at {unit} Level")
    autocorrelation_plot(time_series)
    plt.show()

# Summarize results
summary = pd.DataFrame(results).T
summary.index.name = "Temporal Unit"
summary.reset_index(inplace=True)

print("Results across temporal units:")
import ace_tools as tools; tools.display_dataframe_to_user(name="Temporal Unit Analysis Results", dataframe=summary)
