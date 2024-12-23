# Step 1: Out-of-Fold Predictions for Calibration

from sklearn.model_selection import StratifiedKFold
import numpy as np

# Cross-validation setup
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

# Placeholder for out-of-fold predictions
oof_probs = np.zeros(len(X_train_selected))

for train_idx, val_idx in cv.split(X_train_selected, y_train):
    # Split training data into training and validation folds
    X_train_fold, X_val_fold = X_train_selected.iloc[train_idx], X_train_selected.iloc[val_idx]
    y_train_fold, y_val_fold = y_train.iloc[train_idx], y_train.iloc[val_idx]

    # Create CatBoost Pools for the fold
    train_pool_fold = Pool(
        data=X_train_fold,
        label=y_train_fold,
        cat_features=updated_cat_features,
        text_features=updated_text_features,
        feature_names=list(X_train_fold.columns)
    )
    val_pool_fold = Pool(
        data=X_val_fold,
        label=y_val_fold,
        cat_features=updated_cat_features,
        text_features=updated_text_features,
        feature_names=list(X_val_fold.columns)
    )

    # Train a CatBoost model on the fold
    model_fold = CatBoostClassifier(**best_params)
    model_fold.fit(train_pool_fold, eval_set=val_pool_fold, verbose=100, early_stopping_rounds=50)

    # Predict probabilities for the validation fold
    oof_probs[val_idx] = model_fold.predict_proba(val_pool_fold)[:, 1]

# Out-of-fold predictions are now ready for calibration

# Step 2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from betacal import BetaCalibration
import ml_insights as mli
from itertools import product

# Placeholder for results
calibration_results = []

# Define SplineCalib parameter grid
reg_params = np.logspace(-4, 2, 10)  # Regularization parameters
logodds_eps_values = [1e-7, 1e-5, 1e-3]  # Log-odds epsilon values
knot_sample_sizes = [10, 20, 30]  # Number of knots to sample
unity_prior_weights = [None, 10, 25, 50]  # Unity prior weights

spline_parameter_grid = list(
    product(reg_params, logodds_eps_values, knot_sample_sizes, unity_prior_weights)
)

# Define uncalibrated probabilities and targets
# These should come from your previously trained CatBoost model
# Use out-of-fold predictions for the training set and predictions for the test set
oof_probs = oof_probs  # Out-of-fold predictions (from CV)
y_train = y_train      # Training labels
y_test = y_test        # Test labels
y_test_pred_uncalib = y_test_pred_uncalib  # Uncalibrated test set probabilities

# ----- Uncalibrated -----
uncalibrated_log_loss = log_loss(y_test, y_test_pred_uncalib)
calibration_results.append({"Method": "Uncalibrated", "Log-Loss": uncalibrated_log_loss})

# ----- Platt Scaling -----
platt_calibrator = LogisticRegression(C=1e10, solver='lbfgs', max_iter=5000)
platt_calibrator.fit(oof_probs.reshape(-1, 1), y_train)
y_test_pred_platt = platt_calibrator.predict_proba(y_test_pred_uncalib.reshape(-1, 1))[:, 1]
platt_log_loss = log_loss(y_test, y_test_pred_platt)
calibration_results.append({"Method": "Platt Scaling", "Log-Loss": platt_log_loss})

# ----- Isotonic Regression -----
iso_calibrator = IsotonicRegression(out_of_bounds="clip")
iso_calibrator.fit(oof_probs, y_train)
y_test_pred_iso = iso_calibrator.predict(y_test_pred_uncalib)
iso_log_loss = log_loss(y_test, y_test_pred_iso)
calibration_results.append({"Method": "Isotonic Regression", "Log-Loss": iso_log_loss})

# ----- Beta Calibration -----
beta_calibrator = BetaCalibration()
beta_calibrator.fit(oof_probs, y_train)
y_test_pred_beta = beta_calibrator.predict(y_test_pred_uncalib)
beta_log_loss = log_loss(y_test, y_test_pred_beta)
calibration_results.append({"Method": "Beta Calibration", "Log-Loss": beta_log_loss})

# ----- Spline Calibration (Multiple Configurations) -----
spline_results = []
for i, (reg_param, logodds_eps, knot_sample_size, unity_prior_weight) in enumerate(spline_parameter_grid):
    print(f"Testing Spline configuration {i + 1}/{len(spline_parameter_grid)}...")

    # Initialize SplineCalib with the current configuration
    sc = mli.SplineCalib(
        reg_param_vec=[reg_param],
        logodds_eps=logodds_eps,
        knot_sample_size=knot_sample_size,
        unity_prior=bool(unity_prior_weight),
        unity_prior_weight=unity_prior_weight,
    )

    try:
        # Fit SplineCalib on the training data (out-of-fold predictions)
        sc.fit(oof_probs, y_train)

        # Calibrate the test set probabilities
        y_test_pred_spline = sc.calibrate(y_test_pred_uncalib)

        # Calculate log-loss
        spline_log_loss = log_loss(y_test, y_test_pred_spline)

        # Store results
        spline_results.append({
            "Configuration": {
                "reg_param": reg_param,
                "logodds_eps": logodds_eps,
                "knot_sample_size": knot_sample_size,
                "unity_prior_weight": unity_prior_weight,
            },
            "Log-Loss": spline_log_loss
        })

    except Exception as e:
        # Handle cases where Spline calibration fails
        print(f"Spline configuration {i + 1} failed: {e}")

# Add the best SplineCalib result to the main results
if spline_results:
    best_spline_result = min(spline_results, key=lambda x: x["Log-Loss"])
    calibration_results.append({
        "Method": "Spline Calibration (Best Configuration)",
        "Log-Loss": best_spline_result["Log-Loss"],
        "Configuration": best_spline_result["Configuration"]
    })

# ----- Compare Results -----
calibration_results_df = pd.DataFrame(calibration_results)
calibration_results_df = calibration_results_df.sort_values(by="Log-Loss", ascending=True)

# Display the results
print("Calibration Results:")
print(calibration_results_df)

# Plot Reliability Diagrams
plt.figure(figsize=(10, 7))
uncalib_fop, uncalib_mpv = calibration_curve(y_test, y_test_pred_uncalib, n_bins=10, normalize=True)
plt.plot([0, 1], [0, 1], "k--", label="Perfectly Calibrated")
plt.plot(uncalib_mpv, uncalib_fop, marker="o", label="Uncalibrated")

# Add calibrated curves
if platt_log_loss:
    platt_fop, platt_mpv = calibration_curve(y_test, y_test_pred_platt, n_bins=10, normalize=True)
    plt.plot(platt_mpv, platt_fop, marker="o", label="Platt Scaling")
if iso_log_loss:
    iso_fop, iso_mpv = calibration_curve(y_test, y_test_pred_iso, n_bins=10, normalize=True)
    plt.plot(iso_mpv, iso_fop, marker="o", label="Isotonic Regression")
if beta_log_loss:
    beta_fop, beta_mpv = calibration_curve(y_test, y_test_pred_beta, n_bins=10, normalize=True)
    plt.plot(beta_mpv, beta_fop, marker="o", label="Beta Calibration")

# Best Spline Calibration Curve
if spline_results:
    best_spline_config = best_spline_result["Configuration"]
    sc_best = mli.SplineCalib(**best_spline_config)
    sc_best.fit(oof_probs, y_train)
    y_test_pred_best_spline = sc_best.calibrate(y_test_pred_uncalib)
    spline_fop, spline_mpv = calibration_curve(y_test, y_test_pred_best_spline, n_bins=10, normalize=True)
    plt.plot(spline_mpv, spline_fop, marker="o", label="Spline Calibration (Best)")

plt.xlabel("Mean Predicted Probability")
plt.ylabel("Fraction of Positives")
plt.title("Reliability Diagram")
plt.legend()
plt.show()
