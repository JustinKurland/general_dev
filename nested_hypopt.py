import optuna
from sklearn.model_selection import StratifiedKFold
from catboost import CatBoostClassifier, Pool
import numpy as np


def objective(trial, X_train_outer, y_train_outer, cat_features, text_features):
    # Define the parameter space
    params = {
        # Core Parameters
        "iterations": trial.suggest_int("iterations", 500, 2000),
        "depth": trial.suggest_int("depth", 4, 10),
        "learning_rate": trial.suggest_loguniform("learning_rate", 0.005, 0.1),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
        "scale_pos_weight": trial.suggest_float("scale_pos_weight", 50, 150),

        # Categorical Feature Encoding
        "one_hot_max_size": trial.suggest_int("one_hot_max_size", 2, 20),
        "max_ctr_complexity": trial.suggest_int("max_ctr_complexity", 1, 3),
        "ctr_target_border_count": trial.suggest_int("ctr_target_border_count", 1, 255),

        # Text Feature Embeddings
        "text_processing": {
            "tokenizer_type": trial.suggest_categorical("tokenizer_type", ["Space", "Word"]),
            "feature_calcers": trial.suggest_categorical(
                "feature_calcers", [["BoW"], ["BoW", "TF-IDF"], ["NaiveBayes"]]
            ),
        },

        # Regularization and Sampling
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "random_strength": trial.suggest_float("random_strength", 0.1, 10),

        # Tree Optimization
        "border_count": trial.suggest_int("border_count", 32, 255),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 20),

        # Bootstrap Sampling
        "bagging_temperature": trial.suggest_float("bagging_temperature", 0, 1),

        # General
        "loss_function": "Logloss",
        "eval_metric": "Logloss",
        "random_seed": 123,
        "verbose": 0,
    }

    # Inner loop: Stratified K-Fold cross-validation
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=123)
    cv_logloss = []

    for fold_idx, (inner_train_idx, inner_val_idx) in enumerate(inner_cv.split(X_train_outer, y_train_outer)):
        X_inner_train, X_inner_val = X_train_outer.iloc[inner_train_idx], X_train_outer.iloc[inner_val_idx]
        y_inner_train, y_inner_val = y_train_outer.iloc[inner_train_idx], y_train_outer.iloc[inner_val_idx]

        # Create Pool objects
        train_pool = Pool(
            data=X_inner_train,
            label=y_inner_train,
            cat_features=cat_features,
            text_features=text_features,
            feature_names=list(X_inner_train.columns),
        )
        val_pool = Pool(
            data=X_inner_val,
            label=y_inner_val,
            cat_features=cat_features,
            text_features=text_features,
            feature_names=list(X_inner_val.columns),
        )

        # Train CatBoost model
        model = CatBoostClassifier(**params)
        model.fit(train_pool, eval_set=val_pool, use_best_model=True, verbose=0)

        # Evaluate log loss on the validation set
        val_pred_proba = model.predict_proba(val_pool)
        val_logloss = -np.mean(
            y_inner_val * np.log(val_pred_proba[:, 1]) + (1 - y_inner_val) * np.log(val_pred_proba[:, 0])
        )
        cv_logloss.append(val_logloss)

        # Prune unpromising trials
        trial.report(np.mean(cv_logloss), fold_idx)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    # Return the mean log loss across inner folds
    return np.mean(cv_logloss)


# Perform nested CV with Optuna
def nested_cv_optimization(X_train, y_train, cat_features, text_features, n_trials=50):
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)
    best_params_per_fold = []

    for train_idx, val_idx in outer_cv.split(X_train, y_train):
        X_outer_train, X_outer_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_outer_train, y_outer_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

        # Inner loop: Optuna study
        study = optuna.create_study(direction="minimize", pruner=optuna.pruners.MedianPruner())
        study.optimize(
            lambda trial: objective(trial, X_outer_train, y_outer_train, cat_features, text_features),
            n_trials=n_trials,
        )

        # Save best parameters for this fold
        best_params_per_fold.append(study.best_params)
        print(f"Best params for fold: {study.best_params}")

    return best_params_per_fold


# Run optimization
best_params_per_fold = nested_cv_optimization(X_train_selected, y_train, cat_features, text_features, n_trials=50)
