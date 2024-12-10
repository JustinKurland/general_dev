def impute_missing_values(df, time_col, customer_col, time_window, columns_to_impute):
    """
    Imputes missing values in specified columns based on values from the same customer
    within a specified time window. Ensures no rows are dropped.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        time_col (str): Name of the timestamp column.
        customer_col (str): Name of the customer column.
        time_window (timedelta): Time window for finding non-missing values.
        columns_to_impute (list): List of columns to impute.

    Returns:
        pd.DataFrame: DataFrame with missing values imputed.
    """
    # Ensure the time column is a datetime type
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Sort the data by customer and time for consistent processing
    df = df.sort_values(by=[customer_col, time_col])
    
    # Function to fill missing values for a single customer
    def fill_for_customer(customer_data):
        customer_data = customer_data.copy()  # Avoid modifying the original DataFrame
        for col in columns_to_impute:
            for i, row in customer_data.iterrows():
                if pd.isna(row[col]):
                    # Find rows within the time window
                    mask = (customer_data[time_col] >= row[time_col] - time_window) & \
                           (customer_data[time_col] <= row[time_col] + time_window)
                    potential_values = customer_data.loc[mask, col].dropna()
                    if not potential_values.empty:
                        # Use the first non-missing value within the time window
                        customer_data.at[i, col] = potential_values.iloc[0]
        return customer_data
    
    # Apply the function to each customer group
    imputed_df = df.groupby(customer_col, group_keys=False).apply(fill_for_customer)
    
    return imputed_df
