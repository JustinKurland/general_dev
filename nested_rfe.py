from sklearn.model_selection import StratifiedKFold
from catboost import CatBoostClassifier, Pool
import numpy as np

# Outer loop: Stratified K-Fold for feature selection
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

# Store selected features
final_features = []

# Perform nested CV for feature selection
for train_idx, val_idx in outer_cv.split(X_train, y_train):
    X_outer_train, X_outer_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_outer_train, y_outer_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

    # Inner loop: Create CatBoost Pools for training and validation
    train_pool = Pool(
        data=X_outer_train,
        label=y_outer_train,
        cat_features=cat_features,
        text_features=text_features,
        feature_names=list(X_outer_train.columns)
    )
    val_pool = Pool(
        data=X_outer_val,
        label=y_outer_val,
        cat_features=cat_features,
        text_features=text_features,
        feature_names=list(X_outer_val.columns)
    )

    # Initialize CatBoost model
    model = CatBoostClassifier(
        loss_function="Logloss",
        eval_metric="Logloss",
        iterations=500,
        random_seed=123,
        verbose=0
    )

    # Train model and calculate feature importances
    model.fit(train_pool, eval_set=val_pool, use_best_model=True)

    # Get feature importances
    feature_importances = model.get_feature_importance(train_pool)
    feature_names = X_outer_train.columns

    # Rank features based on importance and select non-zero importance
    selected_features = feature_names[np.where(feature_importances > 0)]

    # Append selected features from this fold
    final_features.append(selected_features)

# Consolidate features across all folds
final_features = np.unique(np.concatenate(final_features))

# Filter the dataset to only include selected features
X_train_selected = X_train[final_features]
X_calib_selected = X_calib[final_features]
X_test_selected = X_test[final_features]
