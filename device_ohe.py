# Define the column name
column_name = 'Device Health Reasons'

# Step 1: Preprocess the column to extract the single value from the dictionary format
def preprocess_single_tag(row):
    """
    Extracts the single tag from the dictionary-like string.
    Args:
        row (str): The input row string.
    Returns:
        str: The extracted tag or None if invalid.
    """
    if pd.isna(row) or not isinstance(row, str):
        return None  # Return None for NaN or non-string values

    # Remove curly braces and strip whitespace
    tag = row.replace('{', '').replace('}', '').strip()
    return tag

# Apply preprocessing to extract the single tag
filtered_df['extracted_tag'] = filtered_df[column_name].apply(preprocess_single_tag)

# Step 2: One-hot encode the extracted tags
unique_tags = filtered_df['extracted_tag'].dropna().unique()  # Get unique tags excluding NaN

for tag in unique_tags:
    filtered_df[f"{column_name}_{tag}"] = filtered_df['extracted_tag'].apply(
        lambda x: 1 if x == tag else 0
    )

# Drop the intermediate extracted_tag column if no longer needed
filtered_df = filtered_df.drop(columns=['extracted_tag'])

# Display the resulting DataFrame
print(filtered_df.head())
