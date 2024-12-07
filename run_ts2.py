import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
import pandas_flavor as pf

@pf.register_dataframe_method
def run_time_series_analysis(
    df,
    date_column,
    value_column,
    rule="D",
    agg_func="sum",
    kind="timestamp",
    seasonal_period=7,
    include_decomposition=True,
    plot=True,
    **kwargs
):
    """
    Perform time series analysis, including aggregation, seasonality strength,
    Fourier analysis, and optional decomposition, using `summarize_by_time`.

    Parameters:
    ----------
    df : pd.DataFrame
        The dataset containing the time series data.
    date_column : str
        The column name representing the datetime information.
    value_column : str
        The column name containing the values to analyze.
    rule : str, optional
        A pandas frequency (e.g., "D" for daily, "W" for weekly, "M" for monthly).
        Default is "D".
    agg_func : str, optional
        The aggregation function to summarize the values (e.g., "sum", "mean").
        Default is "sum".
    kind : str, optional
        "timestamp" or "period". Default is "timestamp".
    seasonal_period : int, optional
        The assumed seasonal periodicity (e.g., 7 for weekly data).
        Default is 7.
    include_decomposition : bool, optional
        Whether to include STL decomposition in the analysis.
        Default is True.
    plot : bool, optional
        Whether to plot the analysis results. Default is True.
    **kwargs:
        Additional arguments passed to `summarize_by_time`.

    Returns:
    -------
    results : dict
        A dictionary containing the seasonality strength, dominant frequency,
        residual-to-total variance ratio, and interpretation.
    """
    # Step 1: Aggregate using summarize_by_time
    aggregated_df = df.summarize_by_time(
        date_column=date_column,
        value_column=value_column,
        rule=rule,
        agg_func=agg_func,
        kind=kind,
        **kwargs
    )

    # Convert to a pandas Series for easier time series analysis
    time_series = aggregated_df.squeeze()
    if kind == "period":
        time_series.index = time_series.index.to_timestamp()

    # Step 2: Plot the aggregated time series
    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(time_series.index, time_series.values, marker="o", linestyle="-")
        plt.title(f"Time Series Aggregated by {rule}", fontsize=16)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel(f"{agg_func.capitalize()} of {value_column}", fontsize=14)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Step 3: Decompose the time series (optional)
    results = {}
    if include_decomposition:
        stl = STL(time_series, seasonal=seasonal_period).fit()
        seasonal_var = np.var(stl.seasonal)
        total_var = np.var(time_series)
        residual_var = np.var(stl.resid)

        seasonality_strength = seasonal_var / total_var if total_var != 0 else 0
        residual_to_total_ratio = residual_var / total_var if total_var != 0 else 0

        results["Seasonality Strength"] = seasonality_strength
        results["Residual to Total Ratio"] = residual_to_total_ratio

        # Plot STL decomposition
        if plot:
            fig, axes = plt.subplots(3, 1, figsize=(12, 8))
            stl.seasonal.plot(ax=axes[0], title="Seasonal Component", ylabel="Seasonal", color="blue")
            stl.trend.plot(ax=axes[1], title="Trend Component", ylabel="Trend", color="green")
            stl.resid.plot(ax=axes[2], title="Residual Component", ylabel="Residual", color="red")
            plt.tight_layout()
            plt.show()

    # Step 4: Perform Fourier Transform
    fft_result = np.fft.fft(time_series.values - time_series.values.mean())
    frequencies = np.fft.fftfreq(len(time_series), d=1)
    dominant_frequency = frequencies[np.argmax(np.abs(fft_result))]
    results["Dominant Frequency"] = dominant_frequency

    # Step 5: Interpret the results
    interpretation = []
    if results.get("Seasonality Strength", 0) > 0.8:
        interpretation.append("Strong seasonality detected (seasonality strength > 0.8).")
    else:
        interpretation.append("Weak seasonality detected (seasonality strength <= 0.8).")

    if abs(dominant_frequency) > 0:
        interpretation.append(f"Dominant periodicity detected with a frequency of {dominant_frequency:.2f}.")
    else:
        interpretation.append("No significant dominant periodicity detected.")

    if results.get("Residual to Total Ratio", 0) < 0.1:
        interpretation.append(
            "Low residual variance compared to total variance, indicating systematic patterns."
        )
    else:
        interpretation.append(
            "High residual variance, indicating less systematic patterns in the data."
        )

    results["Interpretation"] = interpretation

    # Print interpretation
    print("\nInterpretation:")
    for line in interpretation:
        print(f"- {line}")

    # Step 6: Plot autocorrelation
    if plot:
        pd.plotting.autocorrelation_plot(time_series)
        plt.title("Autocorrelation Plot")
        plt.show()

    return results
