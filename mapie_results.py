# Step 5: Visualize the prediction sets
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Left: Plot predicted probabilities
axs[0].scatter(range(len(X_test_selected)), y_pred_proba[:, 1], label="Predicted Probability")
axs[0].set_title("Prediction Decision Boundary")
axs[0].set_xlabel("Sample Index")
axs[0].set_ylabel("Predicted Probability")
axs[0].legend()

# Middle: Prediction interval for alpha[idx-1]
if idx > 0:
    _, y_ps = mapie_clf.predict(X_test_selected, alpha=alpha_)
    axs[1].fill_between(
        range(len(X_test_selected)),
        y_ps[:, 0, idx - 1],
        y_ps[:, 1, idx - 1],
        color="gray",
        alpha=0.5,
        label=f"Prediction Interval (alpha={alpha_[idx - 1]:.2f})"
    )
    axs[1].set_title(f"Prediction Interval (alpha={alpha_[idx - 1]:.2f})")
    axs[1].set_xlabel("Sample Index")
    axs[1].set_ylabel("Predicted Probability")
    axs[1].legend()
else:
    axs[1].text(0.5, 0.5, "No valid alpha[idx-1]", transform=axs[1].transAxes, ha="center", va="center")

# Right: Prediction interval for alpha[idx+1]
if idx < len(alpha_) - 1:
    axs[2].fill_between(
        range(len(X_test_selected)),
        y_ps[:, 0, idx + 1],
        y_ps[:, 1, idx + 1],
        color="gray",
        alpha=0.5,
        label=f"Prediction Interval (alpha={alpha_[idx + 1]:.2f})"
    )
    axs[2].set_title(f"Prediction Interval (alpha={alpha_[idx + 1]:.2f})")
    axs[2].set_xlabel("Sample Index")
    axs[2].set_ylabel("Predicted Probability")
    axs[2].legend()
else:
    axs[2].text(0.5, 0.5, "No valid alpha[idx+1]", transform=axs[2].transAxes, ha="center", va="center")

plt.tight_layout()
plt.show()
