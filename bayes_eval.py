# Extract transition probabilities
print("Transition Matrix:")
print(hmm.transmat_)

# Analyze transition behavior
state_counts = np.bincount(states)
state_proportions = state_counts / len(states)

print(f"Proportion of time spent in State 0: {state_proportions[0]:.2f}")
print(f"Proportion of time spent in State 1: {state_proportions[1]:.2f}")


import matplotlib.pyplot as plt

plt.hist(observed_state_0_dwell, bins=10, alpha=0.5, label='State 0 Dwell Times')
plt.hist(observed_state_1_dwell, bins=10, alpha=0.5, label='State 1 Dwell Times')
plt.legend()
plt.title("Distribution of Dwell Times by State")
plt.xlabel("Dwell Time")
plt.ylabel("Frequency")
plt.show()
