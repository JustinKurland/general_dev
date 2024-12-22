from sklearn.model_selection import train_test_split

def get_nested_cv_splits(df):
    # Preprocess the data
    X, y, number_column = preprocess_data_part(df)

    # Initial split: Reserve test set (15%)
    X_train_calib, X_test, y_train_calib, y_test, number_train_calib, number_test = train_test_split(
        X, y, number_column, test_size=0.15, stratify=y, random_state=123
    )

    # Further split: Separate calibration set (15% of remaining training data)
    X_train, X_calib, y_train, y_calib, number_train, number_calib = train_test_split(
        X_train_calib, y_train_calib, number_train_calib, test_size=0.15, stratify=y_train_calib, random_state=123
    )

    return (
        X_train, X_calib, X_test,
        y_train, y_calib, y_test,
        number_train, number_calib, number_test
    )

# Process the dataset
X_train, X_calib, X_test, y_train, y_calib, y_test, number_train, number_calib, number_test = get_nested_cv_splits(df)
