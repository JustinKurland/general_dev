from sklearn.calibration import CalibratedClassifierCV
from mapie.classification import MapieClassifier

# Step 1: Calibrate the model using isotonic regression
calib = CalibratedClassifierCV(
    estimator=catboost_model,  # Replace with your fine-tuned CatBoost model
    method='isotonic',
    cv='prefit'
)
calib.fit(X_train_selected, y_train)

# Step 2: Use MAPIE for conformal prediction
mapie_clf = MapieClassifier(
    estimator=calib, method='lac', cv='prefit', random_state=42
)
mapie_clf.fit(X_calib_selected, y_calib)

# Step 3: Generate prediction intervals on the test set
alpha_ = np.arange(0.02, 0.16, 0.01)
_, y_ps_mapie = mapie_clf.predict(X_test_selected, alpha=alpha_)

# Step 4: Evaluate the prediction intervals
non_empty = np.mean(
    np.any(mapie_clf.predict(X_test_selected, alpha=alpha_)[1], axis=1), axis=0
)
idx = np.argwhere(non_empty < 1)[0, 0]

# Step 5: Visualize the prediction sets
_, axs = plt.subplots(1, 3, figsize=(15, 5))
plot_prediction_decision(y_pred_mapie, axs[0])
_, y_ps = mapie_clf.predict(X_test_selected, alpha=alpha_[idx-1])
plot_prediction_set(y_ps[:, :, 0], np.round(alpha_[idx-1], 3), axs[1])
_, y_ps = mapie_clf.predict(X_test_selected, alpha=alpha_[idx+1])
plot_prediction_set(y_ps[:, :, 0], np.round(alpha_[idx+1], 3), axs[2])

plt.show()
