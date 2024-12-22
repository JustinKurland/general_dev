def get_processed_data(df):
    # Preprocess the data as in your current implementation
    X, y, number_column = preprocess_data_part(df)

    # Initial split: Separate test set (10-15%)
    X_train_val, X_test, y_train_val, y_test, number_train_val, number_test = train_test_split(
        X, y, number_column, test_size=0.15, stratify=y, random_state=123
    )

    # Further split train_val into training and validation sets
    X_train, X_val, y_train, y_val, number_train, number_val = train_test_split(
        X_train_val, y_train_val, number_train_val, test_size=0.2, stratify=y_train_val, random_state=123
    )

    # Final split: Separate calibration set from training set
    X_train, X_calib, y_train, y_calib, number_train, number_calib = train_test_split(
        X_train, y_train, number_train, test_size=0.15, stratify=y_train, random_state=123
    )

    return (
        X_train, X_val, X_calib, X_test,
        y_train, y_val, y_calib, y_test,
        number_train, number_val, number_calib, number_test
    )

# Process the dataset
X_train, X_val, X_calib, X_test, y_train, y_val, y_calib, y_test, number_train, number_val, number_calib, number_test = get_processed_data(df)
