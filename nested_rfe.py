from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from catboost import CatBoostClassifier
import numpy as np

# Outer loop: Stratified K-Fold for feature selection
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

# Feature selection using nested CV
final_features = []

for train_idx, val_idx in outer_cv.split(X_train, y_train):
    X_outer_train, X_outer_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_outer_train, y_outer_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

    # Inner loop for RFECV
    inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)
    model = CatBoostClassifier(
        loss_function="Logloss",
        cat_features=cat_features,
        text_features=text_features,
        verbose=0
    )
    rfecv = RFECV(estimator=model, step=1, cv=inner_cv, scoring="neg_log_loss", verbose=1)

    rfecv.fit(X_outer_train, y_outer_train)
    selected_features = X_outer_train.columns[rfecv.support_]

    # Save selected features
    final_features.append(selected_features)

# Consolidate selected features
final_features = np.unique(np.concatenate(final_features))

# Filter data to keep only selected features
X_train_selected = X_train[final_features]
X_calib_selected = X_calib[final_features]
X_test_selected = X_test[final_features]
