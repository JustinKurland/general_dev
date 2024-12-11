# Define the column name
column_name = 'Account Telephone Global Trust Tags'

# Step 1: Preprocess the column to extract individual tags
def preprocess_tags(row):
    """
    Parses and extracts unique tags from the row.
    Args:
        row (str): The input row string.
    Returns:
        list: A list of extracted tags or an empty list if invalid.
    """
    if pd.isna(row) or not isinstance(row, str):
        return []  # Return empty list for NaN or non-string values

    # Remove curly braces and split by commas
    tags = row.replace('{', '').replace('}', '').split(',')
    # Strip whitespace from each tag
    return [tag.strip() for tag in tags]

# Apply preprocessing to extract tags
filtered_df['parsed_tags'] = filtered_df[column_name].apply(preprocess_tags)

# Step 2: Extract all unique tags
def extract_unique_tags(column):
    """
    Extracts all unique tags from the preprocessed column.
    Args:
        column (pd.Series): The column containing lists of tags.
    Returns:
        set: A set of unique tags.
    """
    unique_tags = set()
    for row in column.dropna():
        unique_tags.update(row)
    return unique_tags

unique_tags = extract_unique_tags(filtered_df['parsed_tags'])

# Step 3: Create one-hot encoded columns for each tag
for tag in unique_tags:
    filtered_df[f"{column_name}_{tag}"] = filtered_df['parsed_tags'].apply(
        lambda x: 1 if tag in x else 0
    )

# Drop the intermediate parsed column if no longer needed
filtered_df = filtered_df.drop(columns=['parsed_tags'])

# Display the resulting DataFrame
print(filtered_df.head())
