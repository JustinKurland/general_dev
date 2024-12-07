def synthesize_final_conclusion(part1_results, part2_results):
    """
    Synthesizes findings from Part I (Seasonality Analysis) and Part II (HMM Analysis)
    to assess the likelihood of automation in the data.

    Parameters:
    ----------
    part1_results : pd.DataFrame
        Consolidated results from Temporal Dynamics and Seasonality Analysis (Part I).
    part2_results : pd.DataFrame
        Consolidated results from Hidden State and Behavioral Transition Analysis (Part II).

    Returns:
    -------
    conclusion : str
        A synthesized conclusion about the likelihood of automation based on both analyses.
    """

    # Step 1: Aggregate Key Metrics
    # Part I: Seasonality strength
    strong_seasonality = part1_results["Seasonality Strength"].mean() > 0.8
    partial_seasonality = any(part1_results["Seasonality Strength"] > 0.8)

    # Part I: Residual variance
    low_residual_variance = part1_results["Residual to Total Ratio"].mean() < 0.1

    # Part I: Dominant frequencies
    consistent_frequencies = all(part1_results["Dominant Frequency"].notna())

    # Part II: HMM Log Likelihood and Transition Matrix
    high_log_likelihood = part2_results["Log Likelihood"].mean() > -1000
    systematic_transitions = any(
        all(value > 0.8 for row in result) for result in part2_results["Transition Matrix"]
    )

    # Part II: Significant dwell time differences
    significant_dwell_differences = any(
        "Significant difference" in findings for findings in part2_results["Significant Findings"]
    )

    # Step 2: Evaluate Evidence
    evidence = {
        "Strong seasonality": strong_seasonality,
        "Partial seasonality": partial_seasonality,
        "Low residual variance": low_residual_variance,
        "Consistent dominant frequencies": consistent_frequencies,
        "High log likelihood of HMM": high_log_likelihood,
        "Systematic state transitions": systematic_transitions,
        "Significant dwell time differences": significant_dwell_differences,
    }

    # Count strong indicators of automation
    positive_indicators = sum(evidence.values())

    # Step 3: Formulate Conclusion
    conclusion = []
    conclusion.append("Final Synthesis of Results:")
    if positive_indicators >= 5:
        conclusion.append(
            "The data exhibits strong evidence of systematic and repetitive behavior consistent with automation."
        )
        conclusion.append(
            "This includes strong seasonality, low residual variance, and significant differences in dwell times."
        )
        conclusion.append("It is highly likely that the observed process is automated.")
    elif 3 <= positive_indicators < 5:
        conclusion.append(
            "The data shows moderate evidence of systematic behavior consistent with automation."
        )
        conclusion.append(
            "While there is some seasonality and systematic state transitions, the evidence is not uniformly strong."
        )
        conclusion.append("It is moderately likely that the observed process is automated.")
    else:
        conclusion.append("The data does not provide strong evidence for systematic behavior or automation.")
        conclusion.append("Observed patterns could be due to natural variability rather than an automated process.")
        conclusion.append("It is unlikely that the observed process is automated.")

    # Append detailed evidence summary
    conclusion.append("\nDetailed Evidence Summary:")
    for metric, result in evidence.items():
        conclusion.append(f"- {metric}: {'Yes' if result else 'No'}")

    return "\n".join(conclusion)

# Assuming `part1_results` and `part2_results` are DataFrames
final_conclusion = synthesize_final_conclusion(all_results_part1, all_results_part2)

print(final_conclusion)
