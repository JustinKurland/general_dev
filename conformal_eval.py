# Calculate interval coverage
coverage = test_prediction_intervals["Within Interval"].mean()

# Calculate average interval width
test_prediction_intervals["Interval Width"] = (
    test_prediction_intervals["Upper Bound"] - test_prediction_intervals["Lower Bound"]
)
average_width = test_prediction_intervals["Interval Width"].mean()

# Display results
print(f"Interval Coverage: {coverage:.4f}")
print(f"Average Interval Width: {average_width:.4f}")

# Analyze coverage at different significance levels
coverage_by_significance = {
    "alpha_0.1": (quantile := np.quantile(calib_nonconformity, 1 - 0.1)),
    "coverage_0.1": (
        (test_prediction_intervals["Predicted Probability"] >= quantile).mean()
    ),
}

print("\nCoverage by Significance Levels:")
for alpha, value in coverage_by_significance.items():
    print(f"{alpha}: {value:.4f}")

# Visualize interval width distribution
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.hist(
    test_prediction_intervals["Interval Width"],
    bins=30,
    color="#0E4978",
    alpha=0.7,
)
plt.title("Distribution of Interval Widths", fontsize=14)
plt.xlabel("Interval Width", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.show()
