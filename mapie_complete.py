# Step 1: Generate calibrated predictions and prediction intervals
y_pred_mapie, y_ps_mapie = mapie_clf.predict(X_test_selected, alpha=alpha_)

# Step 2: Check how often the true label is inside the prediction intervals
within_interval = (y_test >= y_ps_mapie[:, 0, :]) & (y_test <= y_ps_mapie[:, 1, :])
coverage_by_alpha = within_interval.mean(axis=0)

# Step 3: Compute average interval width
interval_width = y_ps_mapie[:, 1, :] - y_ps_mapie[:, 0, :]
average_width_by_alpha = interval_width.mean(axis=0)

# Step 4: Print results
print("Coverage by Alpha:")
for a, coverage in zip(alpha_, coverage_by_alpha):
    print(f"Alpha {a:.2f}: Coverage = {coverage:.4f}")

print("\nAverage Interval Width by Alpha:")
for a, avg_width in zip(alpha_, average_width_by_alpha):
    print(f"Alpha {a:.2f}: Average Width = {avg_width:.4f}")

# Step 5: Visualize Calibration Curve
plt.figure(figsize=(8, 6))
plt.plot(1 - alpha_, coverage_by_alpha, marker="o", label="Observed Coverage")
plt.plot([0, 1], [0, 1], "--", label="Ideal Calibration")
plt.xlabel("Nominal Coverage (1-alpha)")
plt.ylabel("Observed Coverage")
plt.legend()
plt.title("Calibration Curve")
plt.show()
