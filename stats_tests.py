from scipy.stats import ttest_ind, mannwhitneyu

# Extract observed dwell times for each state
observed_state_0_dwell = [t for s, t in zip(states, dwell_times) if s == 0]
observed_state_1_dwell = [t for s, t in zip(states, dwell_times) if s == 1]

# Extract random dwell times for each state
random_state_0_dwell = [t for s, t in zip(random_states, random_dwell_times) if s == 0]
random_state_1_dwell = [t for s, t in zip(random_states, random_dwell_times) if s == 1]

# Perform t-test for each state
t_stat_0, p_value_0 = ttest_ind(observed_state_0_dwell, random_state_0_dwell, equal_var=False)
t_stat_1, p_value_1 = ttest_ind(observed_state_1_dwell, random_state_1_dwell, equal_var=False)

# Perform Mann-Whitney U test for each state
u_stat_0, u_p_value_0 = mannwhitneyu(observed_state_0_dwell, random_state_0_dwell, alternative='two-sided')
u_stat_1, u_p_value_1 = mannwhitneyu(observed_state_1_dwell, random_state_1_dwell, alternative='two-sided')

# Print results
print("T-Test Results:")
print(f"State 0: t-statistic = {t_stat_0:.2f}, p-value = {p_value_0:.4f}")
print(f"State 1: t-statistic = {t_stat_1:.2f}, p-value = {p_value_1:.4f}")

print("\nMann-Whitney U Test Results:")
print(f"State 0: U-statistic = {u_stat_0:.2f}, p-value = {u_p_value_0:.4f}")
print(f"State 1: U-statistic = {u_stat_1:.2f}, p-value = {u_p_value_1:.4f}")
