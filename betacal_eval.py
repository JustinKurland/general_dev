from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss, brier_score_loss
import numpy as np
import pandas as pd

# Initialize StratifiedKFold for cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

# Placeholder for cross-validation results
beta_calibration_cv_results = []

for fold, (train_idx, val_idx) in enumerate(cv.split(X_train_selected, y_train)):
    # Split training data into train and validation folds
    X_train_fold = X_train_selected.iloc[train_idx]
    y_train_fold = y_train.iloc[train_idx]
    X_val_fold = X_train_selected.iloc[val_idx]
    y_val_fold = y_train.iloc[val_idx]
    
    # Get out-of-fold predictions for training fold
    train_pool = Pool(
        data=X_train_fold,
        label=y_train_fold,
        cat_features=updated_cat_features,
        text_features=updated_text_features,
        feature_names=list(X_train_selected.columns),
    )
    
    val_pool = Pool(
        data=X_val_fold,
        label=y_val_fold,
        cat_features=updated_cat_features,
        text_features=updated_text_features,
        feature_names=list(X_train_selected.columns),
    )
    
    # Train the CatBoost model with best hyperparameters
    model = CatBoostClassifier(**best_params)
    model.fit(train_pool, eval_set=val_pool, verbose=0, early_stopping_rounds=50)
    
    # Get uncalibrated probabilities for the validation set
    val_probs_uncalib = model.predict_proba(val_pool)[:, 1]
    
    # Fit Beta Calibration on the training fold
    beta_calibrator = BetaCalibration()
    beta_calibrator.fit(val_probs_uncalib.reshape(-1, 1), y_val_fold)
    
    # Calibrate the probabilities for the validation fold
    val_probs_calib = beta_calibrator.predict(val_probs_uncalib.reshape(-1, 1))
    
    # Calculate metrics for the calibrated probabilities
    fold_log_loss = log_loss(y_val_fold, val_probs_calib)
    fold_brier_score = brier_score_loss(y_val_fold, val_probs_calib)
    
    # Store the results
    beta_calibration_cv_results.append({
        "Fold": fold + 1,
        "Log-Loss": fold_log_loss,
        "Brier-Score": fold_brier_score,
    })

# Convert results to a DataFrame for analysis
beta_calibration_cv_results_df = pd.DataFrame(beta_calibration_cv_results)

# Display the cross-validation results
print("Beta Calibration Cross-Validation Results:")
print(beta_calibration_cv_results_df)

# Calculate mean and standard deviation of metrics across folds
mean_log_loss = beta_calibration_cv_results_df["Log-Loss"].mean()
std_log_loss = beta_calibration_cv_results_df["Log-Loss"].std()
mean_brier_score = beta_calibration_cv_results_df["Brier-Score"].mean()
std_brier_score = beta_calibration_cv_results_df["Brier-Score"].std()

print("\nMean and Std Dev Across Folds:")
print(f"Log-Loss: {mean_log_loss:.4f} ± {std_log_loss:.4f}")
print(f"Brier-Score: {mean_brier_score:.4f} ± {std_brier_score:.4f}")
