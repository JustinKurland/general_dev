# Visualize the first 100 prediction intervals
import matplotlib.pyplot as plt

subset = test_prediction_intervals.head(100)

plt.figure(figsize=(10, 6))
plt.plot(subset.index, subset["Predicted Probability"], label="Predicted Probability", color="blue")
plt.fill_between(
    subset.index,
    subset["Lower Bound"],
    subset["Upper Bound"],
    color="gray",
    alpha=0.3,
    label="Prediction Interval",
)
plt.scatter(
    subset.index,
    subset["True Label"],
    color="red",
    label="True Label",
    zorder=5,
)
plt.title("Prediction Intervals and True Labels")
plt.xlabel("Sample Index")
plt.ylabel("Probability")
plt.legend()
plt.show()
