def calculate_missingness(df):
    """
    Calculates the count and percentage of missing values per column in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame showing the count and percentage of missing values per column.
    """
    missing_count = df.isnull().sum()  # Count of missing values per column
    missing_percentage = (missing_count / len(df)) * 100  # Percentage of missing values per column

    # Combine results into a new DataFrame
    missingness_df = pd.DataFrame({
        'Missing Count': missing_count,
        'Missing Percentage': missing_percentage
    }).sort_values(by='Missing Percentage', ascending=False)  # Sort by percentage

    return missingness_df

# Example usage
missingness_report = calculate_missingness(df)
print(missingness_report)
