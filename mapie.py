from mapie.classification import MapieClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

# Step 1: Create a wrapper for the best CatBoost model
class CatBoostSklearnWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, catboost_model):
        self.catboost_model = catboost_model

    def fit(self, X, y):
        self.catboost_model.fit(X, y)
        return self

    def predict(self, X):
        return self.catboost_model.predict(X)

    def predict_proba(self, X):
        return self.catboost_model.predict_proba(X)

# Wrap the best CatBoost model
catboost_wrapper = CatBoostSklearnWrapper(catboost_model=model)  # 'model' is your fine-tuned CatBoostClassifier

# Step 2: Apply beta calibration using out-of-fold predictions
beta_calibrator.fit(
    oof_probs.reshape(-1, 1),  # Out-of-fold uncalibrated probabilities
    y_train
)

# Step 3: Use the beta-calibrated model for MAPIE
class BetaCalibratedWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, base_model, calibrator):
        self.base_model = base_model
        self.calibrator = calibrator

    def fit(self, X, y):
        self.base_model.fit(X, y)
        return self

    def predict(self, X):
        return self.base_model.predict(X)

    def predict_proba(self, X):
        uncalibrated_probs = self.base_model.predict_proba(X)[:, 1]
        calibrated_probs = self.calibrator.predict(uncalibrated_probs.reshape(-1, 1))
        return np.column_stack([1 - calibrated_probs, calibrated_probs])

# Combine the best CatBoost model with beta calibration
beta_calibrated_model = BetaCalibratedWrapper(base_model=catboost_wrapper, calibrator=beta_calibrator)

# Step 4: Fit MAPIE using calibration data
mapie_clf = MapieClassifier(estimator=beta_calibrated_model, method="score", cv="prefit", n_jobs=-1)
mapie_clf.fit(X_calib_selected, y_calib)  # Calibration data

# Step 5: Generate prediction intervals on the test set
alpha = [0.1]  # For 90% confidence
y_pred_mapie, y_ps_mapie = mapie_clf.predict(X_test_selected, alpha=alpha)

# Step 6: Organize prediction intervals into a DataFrame
test_prediction_intervals = pd.DataFrame(
    {
        "Lower Bound": y_ps_mapie[:, 0, 0],
        "Upper Bound": y_ps_mapie[:, 0, 1],
        "Predicted Probability": beta_calibrator.predict_proba(y_pred_proba[:, 1].reshape(-1, 1))[:, 1],
        "True Label": y_test,
        "Within Interval": (
            (y_test >= y_ps_mapie[:, 0, 0]) & (y_test <= y_ps_mapie[:, 0, 1])
        ),
    }
)

# Step 7: Evaluate intervals
coverage = test_prediction_intervals["Within Interval"].mean()
average_width = (
    test_prediction_intervals["Upper Bound"] - test_prediction_intervals["Lower Bound"]
).mean()

print(f"Interval Coverage: {coverage:.4f}")
print(f"Average Interval Width: {average_width:.4f}")

# Step 8: Visualize interval width distribution
plt.figure(figsize=(8, 6))
plt.hist(
    test_prediction_intervals["Upper Bound"] - test_prediction_intervals["Lower Bound"],
    bins=30,
    color="#0E4978",
    alpha=0.7,
)
plt.title("Distribution of Interval Widths", fontsize=14)
plt.xlabel("Interval Width", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.show()
