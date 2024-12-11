def combine_matching_rows(df, session_id_col, time_col, columns_to_combine):
    """
    Combines rows with the same sessionId by concatenating values in specified columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        session_id_col (str): The column name for session IDs.
        time_col (str): The column name for timestamps.
        columns_to_combine (list): List of columns to combine data for.

    Returns:
        pd.DataFrame: DataFrame with combined data, preserving unique time values.
    """
    # Group by sessionId and concatenate non-NaN values for specified columns
    combined_data = df.groupby(session_id_col).agg(
        {
            **{col: lambda x: '|'.join(x.dropna().astype(str).unique()) for col in columns_to_combine},
            time_col: list  # Keep all time values as a list
        }
    ).reset_index()

    # Explode the time column to create one row per time value
    combined_data = combined_data.explode(time_col).reset_index(drop=True)

    return combined_data

# Example usage
columns_to_combine = ['action', 'TMX_device_id']

# Apply the function
combined_df = combine_matching_rows(
    df, 
    session_id_col='sessionId', 
    time_col='time', 
    columns_to_combine=columns_to_combine
)

# Validate results
print(f"Original rows: {len(df)}")
print(f"Combined rows: {len(combined_df)}")
