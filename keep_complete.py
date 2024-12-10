def keep_most_complete_rows(df, key):
    # Calculate the number of non-null values for each row
    df['non_null_count'] = df.notna().sum(axis=1)

    # Sort rows by sessionID and non_null_count (descending)
    sorted_df = df.sort_values(by=[key, 'non_null_count'], ascending=[True, False])

    # Drop duplicate sessionIDs, keeping the most complete row
    most_complete_df = sorted_df.drop_duplicates(subset=[key], keep='first').drop(columns=['non_null_count'])

    return most_complete_df

# Example usage
most_complete_rows = keep_most_complete_rows(result, key='sessionID')

# Display the resulting DataFrame
most_complete_rows
