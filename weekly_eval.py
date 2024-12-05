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

# Ensure the weekly_counts_series is converted to a numeric numpy array
weekly_counts_array = weekly_counts_series.to_numpy()

# Fourier Transform
fft_result = fft(weekly_counts_array - weekly_counts_array.mean())
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

# Interpret Results
interpretation = []
if seasonality_strength > 0.8:
    interpretation.append(
        "Strong seasonality detected (seasonality strength > 0.8). This suggests "
        "a highly repetitive pattern, potentially indicative of an automated process."
    )
else:
    interpretation.append(
        "Seasonality strength is weak (<= 0.8), suggesting limited repetitive patterns."
    )

if abs(dominant_frequency) > 0:
    interpretation.append(
        f"A dominant periodicity was detected with a frequency of {dominant_frequency:.2f}. "
        "This further supports evidence of a recurring cycle."
    )
else:
    interpretation.append(
        "No significant dominant periodicity detected, reducing the likelihood of automation."
    )

if residual_to_total_ratio < 0.1:
    interpretation.append(
        "The residual variance is very small compared to total variance, meaning most of the variation is explained "
        "by predictable components. This strengthens the case for a systematic or automated pattern."
    )
else:
    interpretation.append(
        "Residual variance is relatively high, indicating a lack of systematic patterns in the data."
    )

print("\nInterpretation:")
for line in interpretation:
    print(f"- {line}")

# Plot Decomposition (enlarged)
fig, axes = plt.subplots(3, 1, figsize=(12, 8))  # Enlarged for clarity
stl.seasonal.plot(ax=axes[0], title="Seasonal Component", ylabel="Seasonal", color="blue")
stl.trend.plot(ax=axes[1], title="Trend Component", ylabel="Trend", color="green")
stl.resid.plot(ax=axes[2], title="Residual Component", ylabel="Residual", color="red")
plt.tight_layout()
plt.show()

# Autocorrelation Plot
print("Autocorrelation Plot for Weekly Data:")
autocorrelation_plot(weekly_counts_series)
plt.show()
