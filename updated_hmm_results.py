def combine_hmm_results(hmm_results):
    """
    Combines HMM results across different temporal units into a unified DataFrame
    and synthesizes insights.

    Parameters:
    ----------
    hmm_results : dict
        A dictionary where keys are temporal units (e.g., "Minute", "Hour") and
        values are the respective HMM analysis results dictionaries.

    Returns:
    -------
    combined_results : pd.DataFrame
        A DataFrame summarizing the results for all temporal units.
    synthesis : str
        A synthesized interpretation of the results across temporal units.
    """
    combined_data = []
    all_feedback = []
    for unit, result in hmm_results.items():
        # Ensure State Proportions is a list/tuple and extract feedback
        state_proportions = result.get("State Proportions", [])
        if not isinstance(state_proportions, (list, tuple)):
            state_proportions = [state_proportions]

        # Append relevant metrics
        combined_data.append({
            "Temporal Unit": unit,
            "Log Likelihood": result.get("Log Likelihood", "N/A"),
            "State Proportions": state_proportions,
            "Significant Findings": ", ".join(result.get("Feedback", [])),
        })
        all_feedback.extend(result.get("Feedback", []))

    # Convert combined data to a DataFrame
    combined_results = pd.DataFrame(combined_data)

    # Synthesize insights
    synthesis = []

    # Check for significant findings across temporal units
    significant_units = [unit for unit, result in hmm_results.items() if result.get("Feedback")]
    if significant_units:
        synthesis.append(
            f"Significant findings were observed for the following temporal units: {', '.join(significant_units)}."
        )
    else:
        synthesis.append("No significant findings were observed across any temporal unit.")

    # Check for consistency in state proportions
    try:
        consistent_state_proportions = len(set(tuple(result.get("State Proportions", [])) for result in hmm_results.values())) == 1
    except TypeError:
        consistent_state_proportions = False

    if consistent_state_proportions:
        synthesis.append("State proportions are consistent across all temporal units, suggesting uniform behavior.")
    else:
        synthesis.append("State proportions vary across temporal units, suggesting potential differences in granularity.")

    # Provide final interpretation
    synthesis.append(
        "Overall, the results suggest systematic behavior consistent with automation."
        if any("Significant difference" in feedback for feedback in all_feedback)
        else "The results do not provide strong evidence for systematic behavior or automation."
    )

    return combined_results, "\n".join(synthesis)
