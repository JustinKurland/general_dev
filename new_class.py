@pd.api.extensions.register_dataframe_accessor("analyze")
class TimeSeriesAnalyzer:
    """
    A pandas accessor for performing time series analysis on a DataFrame
    by summarizing data with the `summarize_by_time` function and adding
    additional trend and seasonality analysis.
    """

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def time_series(
        self,
        date_column,
        value_column,
        frequency="M",
        summarize_func="mean",
        include_trend_analysis=True,
        include_seasonality_analysis=True,
        plot=True,
        custom_freq=None
    ):
        """
        Analyze a time series dataset using `summarize_by_time` for summarization
        and adding optional trend and seasonality analysis.

        Parameters:
        ----------
        date_column : str
            The column name representing the datetime information.
        value_column : str
            The column name containing the values to analyze.
        frequency : str, optional
            The temporal frequency for summarization (e.g., 'M', 'W', 'D').
            Default is 'M'.
        summarize_func : str, optional
            The aggregation function to summarize the values (e.g., 'mean', 'sum').
            Default is 'mean'.
        include_trend_analysis : bool, optional
            Whether to include trend analysis (mean, std_dev, etc.).
            Default is True.
        include_seasonality_analysis : bool, optional
            Whether to include seasonality analysis.
            Default is True.
        plot : bool, optional
            Whether to plot the summarized data and results.
            Default is True.
        custom_freq : str, optional
            A custom frequency string for summarization (e.g., '3M').
            Overrides `frequency` if provided.

        Returns:
        -------
        summary_df : pd.DataFrame
            A DataFrame containing the summarized time series data.
        analysis_results : dict
            A dictionary containing the results of trend and seasonality analysis.
        """
        # Call summarize_by_time function
        freq = custom_freq if custom_freq else frequency
        summary_df = self._obj.summarize_by_time(
            date_column=date_column,
            value_column=value_column,
            freq=freq,
            agg_func=summarize_func,
        )

        # Perform additional analysis
        analysis_results = {}

        # Trend analysis
        if include_trend_analysis:
            trend_analysis = {}
            trend_analysis["mean"] = summary_df[f"{summarize_func}_{value_column}"].mean()
            trend_analysis["std_dev"] = summary_df[f"{summarize_func}_{value_column}"].std()

            autocorrelation = np.corrcoef(
                summary_df[f"{summarize_func}_{value_column}"][:-1],
                summary_df[f"{summarize_func}_{value_column}"][1:]
            )[0, 1]
            trend_analysis["autocorrelation"] = autocorrelation

            detrended = np.gradient(summary_df[f"{summarize_func}_{value_column}"])
            trend_analysis["detrended_std"] = np.std(detrended)

            analysis_results["trend_analysis"] = trend_analysis

        # Seasonality analysis
        if include_seasonality_analysis:
            seasonality_analysis = {}
            frequencies = np.fft.fftfreq(len(summary_df), d=1)
            fft_values = np.fft.fft(summary_df[f"{summarize_func}_{value_column}"])
            dominant_freq_idx = np.argmax(np.abs(fft_values[1:])) + 1
            dominant_frequency = frequencies[dominant_freq_idx]
            seasonality_analysis["dominant_frequency"] = dominant_frequency

            analysis_results["seasonality_analysis"] = seasonality_analysis

        # Plot results
        if plot:
            plt.figure(figsize=(10, 6))
            plt.plot(summary_df[date_column], summary_df[f"{summarize_func}_{value_column}"], label="Summary")
            if include_trend_analysis:
                plt.axhline(
                    analysis_results["trend_analysis"]["mean"],
                    color="red",
                    linestyle="--",
                    label="Mean"
                )
            plt.title(f"Time Series Analysis ({freq})")
            plt.xlabel("Date")
            plt.ylabel(f"{summarize_func.capitalize()} of {value_column}")
            plt.legend()
            plt.show()

        return summary_df, analysis_results
