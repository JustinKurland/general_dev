def combine_matching_rows_full(df, session_id_col, time_col, columns_to_combine):
    """
    Combines rows with the same sessionId by concatenating values in specified columns,
    ensuring all rows are retained with their original time values.

    Args:
        df (pd.DataFrame): The input DataFrame.
        session_id_col (str): The column name for session IDs.
        time_col (str): The column name for timestamps.
        columns_to_combine (list): List of columns to combine data for.

    Returns:
        pd.DataFrame: DataFrame with combined data, preserving unique time values.
    """
    # Sort the DataFrame by sessionId and time for proper grouping
    df = df.sort_values(by=[session_id_col, time_col]).reset_index(drop=True)

    # Group by sessionId and concatenate values for specified columns
    grouped = df.groupby(session_id_col).agg(
        {
            **{col: lambda x: '|'.join(x.dropna().astype(str).unique()) for col in columns_to_combine},
        }
    ).reset_index()

    # Merge the grouped data back with the original DataFrame to retain all rows and time values
    merged_df = df[[session_id_col, time_col]].merge(
        grouped, on=session_id_col, how="left"
    )

    return merged_df


# Example usage
columns_to_combine = ['action', 'TMX_device_id']

# Apply the function
combined_df = combine_matching_rows_full(
    df,
    session_id_col='sessionId',
    time_col='time',
    columns_to_combine=columns_to_combine
)

# Validate results
print(f"Original rows: {len(df)}")
print(f"Combined rows: {len(combined_df)}")
