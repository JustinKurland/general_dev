import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from itertools import groupby
from scipy.stats import ttest_ind, mannwhitneyu, ks_2samp

def analyze_hidden_markov_states(
    time_series,
    n_components=2,
    n_iter=100,
    random_state=42,
    plot=True
):
    """
    Analyze time series data using a Hidden Markov Model (HMM) to identify patterns,
    dwell times, and state transitions. Performs statistical tests to assess the hypothesis
    of systematic behavior (e.g., automation).

    Parameters:
    ----------
    time_series : pandas.Series or numpy.ndarray
        The input time series data.
    n_components : int, optional
        The number of hidden states in the HMM. Default is 2.
    n_iter : int, optional
        The maximum number of iterations for the HMM. Default is 100.
    random_state : int, optional
        Seed for reproducibility. Default is 42.
    plot : bool, optional
        Whether to generate plots for HMM states and statistical analysis. Default is True.

    Returns:
    -------
    results : dict
        A dictionary containing HMM metrics, dwell time analysis, statistical test results,
        and interpretative feedback.
    """
    # Step 1: Fit a Hidden Markov Model
    observed_data = time_series.values.reshape(-1, 1)
    hmm = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=n_iter, random_state=random_state)
    hmm.fit(observed_data)
    log_likelihood = hmm.score(observed_data)
    transition_matrix = hmm.transmat_

    # Step 2: Predict states
    states = hmm.predict(observed_data)

    # Step 3: Analyze dwell times for each state
    dwell_times = [len(list(group)) for _, group in groupby(states)]
    dwell_time_by_state = {
        s: [len(list(group)) for state, group in groupby(states) if state == s]
        for s in range(n_components)
    }

    # Step 4: Generate random states for comparison
    random_states = np.random.choice(range(n_components), size=len(states))
    random_dwell_time_by_state = {
        s: [len(list(group)) for state, group in groupby(random_states) if state == s]
        for s in range(n_components)
    }

    # Step 5: Perform statistical tests
    stat_tests = {}
    for state in range(n_components):
        observed_dwell = dwell_time_by_state[state]
        random_dwell = random_dwell_time_by_state[state]

        t_stat, t_p_value = ttest_ind(observed_dwell, random_dwell, equal_var=False)
        u_stat, u_p_value = mannwhitneyu(observed_dwell, random_dwell, alternative="two-sided")
        ks_stat, ks_p_value = ks_2samp(observed_dwell, random_dwell)

        stat_tests[state] = {
            "t-test": {"t_stat": t_stat, "p_value": t_p_value},
            "Mann-Whitney U": {"u_stat": u_stat, "p_value": u_p_value},
            "KS Test": {"ks_stat": ks_stat, "p_value": ks_p_value},
        }

    # Step 6: Analyze state proportions
    state_counts = np.bincount(states, minlength=n_components)
    state_proportions = state_counts / len(states)

    # Step 7: Interpret results
    feedback = []
    for state, stats in stat_tests.items():
        if stats["t-test"]["p_value"] < 0.05:
            feedback.append(f"State {state}: Significant difference in dwell times (t-test, p < 0.05).")
        if stats["Mann-Whitney U"]["p_value"] < 0.05:
            feedback.append(f"State {state}: Significant difference in dwell times (Mann-Whitney U, p < 0.05).")
        if stats["KS Test"]["p_value"] < 0.05:
            feedback.append(f"State {state}: Significant difference in dwell times (KS Test, p < 0.05).")

    if not feedback:
        feedback.append("No significant differences detected in state dwell times. Systematic behavior not evident.")

    # Step 8: Plot results
    if plot:
        # Plot state sequence
        plt.figure(figsize=(10, 6))
        plt.plot(time_series.index, states, marker="o", linestyle="-", label="HMM States")
        plt.title("HMM State Sequence")
        plt.xlabel("Time")
        plt.ylabel("State")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Plot dwell time distribution
        plt.figure(figsize=(10, 6))
        for state in range(n_components):
            plt.hist(
                dwell_time_by_state[state],
                bins=10,
                alpha=0.5,
                label=f"State {state} Dwell Times"
            )
        plt.title("Dwell Time Distribution by State")
        plt.xlabel("Dwell Time")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    # Combine results into a dictionary
    results = {
        "Log Likelihood": log_likelihood,
        "Transition Matrix": transition_matrix,
        "State Proportions": state_proportions.tolist(),
        "Dwell Times": dwell_time_by_state,
        "Statistical Tests": stat_tests,
        "Feedback": feedback,
    }

    return results
