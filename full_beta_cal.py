from sklearn.metrics import log_loss, brier_score_loss, roc_auc_score, calibration_curve
import matplotlib.pyplot as plt

# Train CatBoost on the entire training dataset
final_train_pool = Pool(
    data=X_train_selected,
    label=y_train,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_train_selected.columns),
)

final_model = CatBoostClassifier(**best_params)
final_model.fit(final_train_pool, verbose=100)

# Generate uncalibrated probabilities for the test set
test_pool = Pool(
    data=X_test_selected,
    label=y_test,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_test_selected.columns),
)

y_test_pred_uncalib = final_model.predict_proba(test_pool)[:, 1]

# Apply beta calibration to the test set predictions
beta_calibrator = BetaCalibration()
beta_calibrator.fit(y_test_pred_uncalib.reshape(-1, 1), y_test)
y_test_pred_calib = beta_calibrator.predict(y_test_pred_uncalib.reshape(-1, 1))

# Calculate evaluation metrics
test_log_loss_uncalib = log_loss(y_test, y_test_pred_uncalib)
test_log_loss_calib = log_loss(y_test, y_test_pred_calib)
test_brier_score_uncalib = brier_score_loss(y_test, y_test_pred_uncalib)
test_brier_score_calib = brier_score_loss(y_test, y_test_pred_calib)
test_roc_auc = roc_auc_score(y_test, y_test_pred_calib)

print("\nTest Set Evaluation Results:")
print(f"Uncalibrated Log-Loss: {test_log_loss_uncalib:.4f}")
print(f"Calibrated Log-Loss: {test_log_loss_calib:.4f}")
print(f"Uncalibrated Brier-Score: {test_brier_score_uncalib:.4f}")
print(f"Calibrated Brier-Score: {test_brier_score_calib:.4f}")
print(f"Calibrated ROC-AUC: {test_roc_auc:.4f}")

# Reliability Diagram
uncalib_fop, uncalib_mpv = calibration_curve(y_test, y_test_pred_uncalib, n_bins=10, normalize=True)
calib_fop, calib_mpv = calibration_curve(y_test, y_test_pred_calib, n_bins=10, normalize=True)

plt.figure(figsize=(8, 6))
plt.plot([0, 1], [0, 1], linestyle="--", color="black", label="Perfectly Calibrated")
plt.plot(uncalib_mpv, uncalib_fop, marker=".", label="Uncalibrated", color="#0E4978")
plt.plot(calib_mpv, calib_fop, marker=".", label="Beta Calibration", color="#FFB81C")
plt.title("Reliability Diagram")
plt.xlabel("Mean Predicted Probability")
plt.ylabel("Fraction of Positives")
plt.legend(loc="best")
plt.show()
