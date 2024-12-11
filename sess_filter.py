def filter_sessionid_groups(df, session_id_col, matched_col):
    """
    Filters rows by sessionId groups:
    - For groups with multiple rows, keeps only the row where `matched` equals True.
    - For groups with a single row, retains the row regardless of the `matched` value.

    Args:
        df (pd.DataFrame): The input DataFrame.
        session_id_col (str): The column name for session IDs.
        matched_col (str): The column name indicating whether the row is matched.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # Function to process each group
    def process_group(group):
        if len(group) > 1:  # For groups with multiple rows
            # Keep only the rows where `matched` is True
            filtered_group = group[group[matched_col] == True]
            # If no rows have `matched=True`, keep all rows in the group
            return filtered_group if not filtered_group.empty else group
        else:
            # For single-row groups, keep the row as-is
            return group

    # Apply the function to each group
    filtered_df = df.groupby(session_id_col, group_keys=False).apply(process_group)

    return filtered_df.reset_index(drop=True)
