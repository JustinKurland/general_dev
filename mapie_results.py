# Define alpha values for confidence levels
alpha_ = np.arange(0.02, 0.16, 0.01)

# Generate predictions using MAPIE
_, y_ps_mapie = mapie_clf.predict(X_test_selected, alpha=alpha_)

# Identify the alpha index for which the prediction sets are non-empty
non_empty = np.mean(np.any(y_ps_mapie, axis=1), axis=0)
idx = np.argwhere(non_empty < 1)[0, 0]

# Visualization of prediction sets
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Left: Plot predicted probabilities
axs[0].scatter(range(len(X_test_selected)), y_pred_proba[:, 1], label="Predicted Probability")
axs[0].set_title("Prediction Decision Boundary")
axs[0].set_xlabel("Sample Index")
axs[0].set_ylabel("Predicted Probability")
axs[0].legend()

# Middle: Prediction interval for alpha[idx-1]
_, y_ps = mapie_clf.predict(X_test_selected, alpha=alpha_[idx - 1])
axs[1].fill_between(
    range(len(X_test_selected)),
    y_ps[:, 0, 0],
    y_ps[:, 0, 1],
    color="gray",
    alpha=0.5,
    label=f"Prediction Interval (alpha={alpha_[idx - 1]:.2f})"
)
axs[1].set_title("Prediction Decision Boundary")
axs[1].set_xlabel("Sample Index")
axs[1].set_ylabel("Predicted Probability")
axs[1].legend()

# Right: Prediction interval for alpha[idx+1]
_, y_ps = mapie_clf.predict(X_test_selected, alpha=alpha_[idx + 1])
axs[2].fill_between(
    range(len(X_test_selected)),
    y_ps[:, 0, 0],
    y_ps[:, 0, 1],
    color="gray",
    alpha=0.5,
    label=f"Prediction Interval (alpha={alpha_[idx + 1]:.2f})"
)
axs[2].set_title("Prediction Decision Boundary")
axs[2].set_xlabel("Sample Index")
axs[2].set_ylabel("Predicted Probability")
axs[2].legend()

plt.tight_layout()
plt.show()
