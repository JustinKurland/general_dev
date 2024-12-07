import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_flavor as pf

@pf.register_dataframe_method
def analyze_time_series(
    df,
    date_column,
    value_column,
    groups=None,
    rule="D",
    agg_func=np.sum,
    kind="timestamp",
    wide_format=True,
    fillna=0,
    include_trend_analysis=True,
    include_seasonality_analysis=True,
    plot=True,
    *args,
    **kwargs
):
    """
    Analyze a time series dataset using `summarize_by_time` for summarization
    and perform optional trend and seasonality analysis.

    Parameters:
    ----------
    df : pd.DataFrame
        The dataset to analyze.
    date_column : str
        The column name representing the datetime information.
    value_column : str or list
        The column name(s) containing the values to analyze.
    groups : str, list, or None, optional
        Columns to group by before resampling. Default is None.
    rule : str, optional
        A pandas frequency (e.g., "D" for daily, "M" for monthly).
        Default is "D".
    agg_func : function or list of functions, optional
        Aggregating functions to apply (e.g., np.sum, np.mean).
        Default is np.sum.
    kind : str, optional
        "timestamp" or "period". Default is "timestamp".
    wide_format : bool, optional
        Whether to return a wide or long format DataFrame. Default is True.
    fillna : int or float, optional
        Value to fill missing data. Default is 0.
    include_trend_analysis : bool, optional
        Whether to include trend analysis. Default is True.
    include_seasonality_analysis : bool, optional
        Whether to include seasonality analysis. Default is True.
    plot : bool, optional
        Whether to plot the summarized data and analysis results. Default is True.
    *args, **kwargs :
        Additional arguments passed to `summarize_by_time`.

    Returns:
    -------
    summary_df : pd.DataFrame
        A DataFrame containing the summarized time series data.
    analysis_results : dict
        A dictionary containing the results of trend and seasonality analysis.
    """

    # Call the `summarize_by_time` function
    summary_df = df.summarize_by_time(
        date_column=date_column,
        value_column=value_column,
        groups=groups,
        rule=rule,
        agg_func=agg_func,
        kind=kind,
        wide_format=wide_format,
        fillna=fillna,
        *args,
        **kwargs
    )

    # Perform additional analysis
    analysis_results = {}

    # Trend analysis
    if include_trend_analysis:
        trend_analysis = {}
        trend_analysis["mean"] = summary_df.mean().mean()
        trend_analysis["std_dev"] = summary_df.std().mean()

        if isinstance(summary_df, pd.DataFrame) and len(summary_df.columns) > 1:
            autocorrelation = np.corrcoef(
                summary_df.iloc[:, 0][:-1],
                summary_df.iloc[:, 0][1:]
            )[0, 1]
        else:
            autocorrelation = summary_df.iloc[:, 0].autocorr()
        trend_analysis["autocorrelation"] = autocorrelation

        detrended = np.gradient(summary_df.values, axis=0)
        trend_analysis["detrended_std"] = np.std(detrended)

        analysis_results["trend_analysis"] = trend_analysis

    # Seasonality analysis
    if include_seasonality_analysis:
        seasonality_analysis = {}
        frequencies = np.fft.fftfreq(len(summary_df), d=1)
        fft_values = np.fft.fft(summary_df.mean(axis=1))
        dominant_freq_idx = np.argmax(np.abs(fft_values[1:])) + 1
        dominant_frequency = frequencies[dominant_freq_idx]
        seasonality_analysis["dominant_frequency"] = dominant_frequency

        analysis_results["seasonality_analysis"] = seasonality_analysis

    # Plot results
    if plot:
        plt.figure(figsize=(10, 6))
        if wide_format and groups is not None:
            for col in summary_df.columns.levels[1]:  # Iterate over grouped columns
                plt.plot(
                    summary_df.index,
                    summary_df.xs(col, axis=1, level=1),
                    label=f"Group: {col}"
                )
        else:
            plt.plot(summary_df.index, summary_df.mean(axis=1), label="Summary")

        if include_trend_analysis:
            plt.axhline(
                analysis_results["trend_analysis"]["mean"],
                color="red",
                linestyle="--",
                label="Mean"
            )
        plt.title(f"Time Series Analysis ({rule})")
        plt.xlabel("Date")
        plt.ylabel(f"Aggregated {value_column}")
        plt.legend()
        plt.show()

    return summary_df, analysis_results
