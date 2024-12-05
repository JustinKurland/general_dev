import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import STL
from scipy.fftpack import fft
from pandas.plotting import autocorrelation_plot

# Assuming `weekly_counts_series` is already a pandas Series with a DatetimeIndex
# Example:
# weekly_counts_series = pd.Series(data=[4151, 6366, 5722, ...], index=pd.to_datetime(['2024-10-14', '2024-10-21', '2024-10-28', ...]))

# Decompose the time series
stl = STL(weekly_counts_series, seasonal=7).fit()  # Weekly periodicity assumed (seasonal=7)

# Compute seasonality strength
seasonal_var = np.var(stl.seasonal)
total_var = np.var(weekly_counts_series)
seasonality_strength = seasonal_var / total_var if total_var != 0 else 0

# Fourier Transform
fft_result = fft(weekly_counts_series - weekly_counts_series.mean())
frequencies = np.fft.fftfreq(len(fft_result))
dominant_frequency = frequencies[np.argmax(np.abs(fft_result))]

# Residual variance ratio
residual_var = np.var(stl.resid)
residual_to_total_ratio = residual_var / total_var if total_var != 0 else 0

# Store results in a dictionary
results = {
    'seasonality_strength': seasonality_strength,
    'dominant_frequency': dominant_frequency,
    'residual_to_total_ratio': residual_to_total_ratio
}

# Print Results
print("Results for Weekly Data:")
print(results)

# Plot Decomposition
stl.plot()
plt.suptitle("STL Decomposition (Weekly Data)", fontsize=16)
plt.show()

# Autocorrelation Plot
print("Autocorrelation Plot for Weekly Data:")
autocorrelation_plot(weekly_counts_series)
plt.show()
