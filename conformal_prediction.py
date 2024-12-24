import numpy as np
import pandas as pd

# Step 1: Calculate Nonconformity Scores for the Calibration Dataset
calib_pool = Pool(
    data=X_calib_selected,
    label=y_calib,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_calib_selected.columns),
)

# Predict calibrated probabilities for the calibration set
y_calib_pred = beta_calibrator.predict(final_model.predict_proba(calib_pool)[:, 1].reshape(-1, 1))

# Calculate nonconformity scores (absolute differences between true labels and predicted probabilities)
calib_nonconformity_scores = np.abs(y_calib - y_calib_pred)

# Step 2: Define the Quantile for the Chosen Significance Level
alpha = 0.1  # Significance level (90% confidence intervals)
quantile = np.quantile(calib_nonconformity_scores, 1 - alpha)

# Step 3: Apply Conformal Prediction to the Test Set
test_nonconformity_scores = beta_calibrator.predict(final_model.predict_proba(test_pool)[:, 1].reshape(-1, 1))

# Generate prediction intervals for the test set
test_prediction_intervals = pd.DataFrame({
    "Lower Bound": np.maximum(0, test_nonconformity_scores - quantile),
    "Upper Bound": np.minimum(1, test_nonconformity_scores + quantile),
    "Predicted Probability": test_nonconformity_scores
})

# Step 4: Evaluate Prediction Intervals
# Check if true labels fall within the prediction intervals
test_prediction_intervals["True Label"] = y_test
test_prediction_intervals["Within Interval"] = (
    (test_prediction_intervals["True Label"] >= test_prediction_intervals["Lower Bound"]) &
    (test_prediction_intervals["True Label"] <= test_prediction_intervals["Upper Bound"])
)

coverage = test_prediction_intervals["Within Interval"].mean()
print(f"Prediction Interval Coverage: {coverage:.2%} (Expected: {(1 - alpha) * 100:.2f}%)")

# Display Example Intervals
print("\nExample Prediction Intervals:")
print(test_prediction_intervals.head())
