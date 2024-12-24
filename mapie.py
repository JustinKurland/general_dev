from mapie.estimators import MapieClassifier
from mapie.conformity_scores import AbsoluteConformityScore

# Step 1: Create a Pool for the calibration set
calib_pool = Pool(
    data=X_calib_selected,
    label=y_calib,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_calib_selected.columns),
)

# Step 2: Predict calibrated probabilities on the calibration set
y_calib_pred_uncalib = model.predict_proba(calib_pool)[:, 1]
y_calib_pred_calib = beta_calibrator.predict(y_calib_pred_uncalib.reshape(-1, 1))

# Step 3: Compute nonconformity scores on the calibration set
calib_nonconformity_scores = np.abs(y_calib - y_calib_pred_calib)

# Step 4: Compute quantile threshold for desired significance level
alpha = 0.1  # Change as needed
quantile = np.quantile(calib_nonconformity_scores, 1 - alpha)

# Step 5: Predict on the test set
test_pool = Pool(
    data=X_test_selected,
    label=y_test,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_test_selected.columns),
)

y_test_pred_uncalib = model.predict_proba(test_pool)[:, 1]
y_test_pred_calib = beta_calibrator.predict(y_test_pred_uncalib.reshape(-1, 1))

# Step 6: Construct prediction intervals on the test set
test_prediction_intervals = pd.DataFrame({
    "Lower Bound": np.maximum(0, y_test_pred_calib - quantile),
    "Upper Bound": np.minimum(1, y_test_pred_calib + quantile),
    "Predicted Probability": y_test_pred_calib,
    "True Label": y_test,
    "Within Interval": (y_test >= np.maximum(0, y_test_pred_calib - quantile)) &
                       (y_test <= np.minimum(1, y_test_pred_calib + quantile))
})

# Display summary statistics
coverage = test_prediction_intervals["Within Interval"].mean()
average_width = (test_prediction_intervals["Upper Bound"] - test_prediction_intervals["Lower Bound"]).mean()

print(f"Interval Coverage: {coverage:.4f}")
print(f"Average Interval Width: {average_width:.4f}")

# Visualize interval width distribution
plt.figure(figsize=(8, 6))
plt.hist(test_prediction_intervals["Upper Bound"] - test_prediction_intervals["Lower Bound"], bins=30, color="#0E4978", alpha=0.7)
plt.title("Distribution of Interval Widths", fontsize=14)
plt.xlabel("Interval Width", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.show()
