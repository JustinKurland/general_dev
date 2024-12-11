def impute_missing_values_in_pairs(df, session_id_col, time_col, columns_to_impute):
    """
    Imputes missing values for rows with matching session IDs that are next to each other.

    Args:
        df (pd.DataFrame): The input DataFrame.
        session_id_col (str): The name of the session ID column.
        time_col (str): The name of the time column.
        columns_to_impute (list): Columns where missing values need to be filled.

    Returns:
        pd.DataFrame: The DataFrame with imputed values.
    """
    # Sort by session ID and time for proper pairing
    df = df.sort_values(by=[session_id_col, time_col]).reset_index(drop=True)

    # Function to impute values within a group
    def impute_group(group):
        for col in columns_to_impute:
            # Forward-fill and backward-fill within the group to fill missing values
            group[col] = group[col].fillna(method='ffill').fillna(method='bfill')
        return group

    # Apply the imputation function to each group
    df = df.groupby(session_id_col, group_keys=False).apply(impute_group)

    return df

# Specify columns to impute
columns_to_impute = ['action', 'TMX_device_id']

# Apply the function
imputed_df = impute_missing_values_in_pairs(df, session_id_col='sessionId', time_col='time', columns_to_impute=columns_to_impute)

# Display the resulting DataFrame
imputed_df
