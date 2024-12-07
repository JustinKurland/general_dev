import pandas as pd

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
    # Step 1: Extract key metrics into a list of dictionaries
    combined_data = []
    all_feedback = []
    for unit, result in hmm_results.items():
        # Flatten and extract relevant data for each temporal unit
        combined_data.append({
            "Temporal Unit": unit,
            "Log Likelihood": result["Log Likelihood"],
            "State Proportions": result["State Proportions"],
            "Significant Findings": ", ".join(result["Feedback"]),
        })
        all_feedback.extend(result["Feedback"])

    # Convert to a DataFrame
    combined_results = pd.DataFrame(combined_data)

    # Step 2: Synthesize insights
    synthesis = []

    # Check for consistent significant findings
    significant_units = [unit for unit, result in hmm_results.items() if result["Feedback"]]
    if significant_units:
        synthesis.append(
            f"Significant findings were observed for the following temporal units: {', '.join(significant_units)}."
        )
    else:
        synthesis.append("No significant findings were observed across any temporal unit.")

    # Examine patterns in state proportions
    consistent_state_proportions = all(
        len(set([tuple(result["State Proportions"]) for result in hmm_results.values()])) == 1
    )
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
