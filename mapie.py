# Import the necessary modules
from mapie.classification import MapieClassifier
from mapie.metrics import classification_coverage_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reuse the calibrated CatBoost model and test data
# Make sure the `model` is the best-calibrated CatBoostClassifier, and the test data is already defined
# `X_test_selected` is your test dataset features
# `y_test` is the true labels for the test set

# Initialize MapieClassifier with the calibrated model
mapie = MapieClassifier(estimator=model, method="naive", cv="prefit")

# Fit Mapie on the training data
mapie.fit(X_train_selected, y_train)

# Generate prediction intervals
alpha = 0.1  # Significance level
y_pred_mapie, y_pis_mapie = mapie.predict(X_test_selected, alpha=alpha)

# Convert prediction intervals into a dataframe
test_prediction_intervals_mapie = pd.DataFrame({
    "Lower Bound": y_pis_mapie[:, 0],
    "Upper Bound": y_pis_mapie[:, 1],
    "Predicted Probability": y_pred_mapie[:, 1],  # Positive class probabilities
    "True Label": y_test,
    "Within Interval": (y_test >= y_pis_mapie[:, 0]) & (y_test <= y_pis_mapie[:, 1])
})

# Evaluate the Conformal Prediction Performance
coverage = classification_coverage_score(y_test, y_pis_mapie[:, 0], y_pis_mapie[:, 1])
average_width = (y_pis_mapie[:, 1] - y_pis_mapie[:, 0]).mean()

print(f"Interval Coverage: {coverage:.4f}")
print(f"Average Interval Width: {average_width:.4f}")

# Visualize Prediction Intervals
plt.figure(figsize=(10, 6))
plt.plot(range(len(test_prediction_intervals_mapie)), test_prediction_intervals_mapie["Predicted Probability"], label="Predicted Probability", color="#0E4978")
plt.fill_between(range(len(test_prediction_intervals_mapie)), 
                 test_prediction_intervals_mapie["Lower Bound"], 
                 test_prediction_intervals_mapie["Upper Bound"], 
                 color="#FFB81C", alpha=0.3, label="Prediction Interval")
plt.scatter(range(len(test_prediction_intervals_mapie)), test_prediction_intervals_mapie["True Label"], color="red", label="True Label", s=10)
plt.xlabel("Sample Index")
plt.ylabel("Probability")
plt.title("Prediction Intervals and True Labels")
plt.legend()
plt.show()
