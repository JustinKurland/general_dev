import ast

# Define the column name
column_name = 'Account Telephone Global Trust Tags'

# Step 1: Parse and preprocess the column
def preprocess_nested_column(row):
    """
    Parses and processes each row containing nested dictionaries.
    Args:
        row (str): The input row string.
    Returns:
        list: A list of parsed dictionaries or an empty list if invalid.
    """
    if pd.isna(row):
        return []  # Return empty list for NaN values

    cleaned_row = []
    try:
        # Parse the entire row as a dictionary or list of dictionaries
        parsed_data = ast.literal_eval(row)
        if isinstance(parsed_data, list):  # If it's a list of dictionaries
            cleaned_row.extend(parsed_data)
        elif isinstance(parsed_data, dict):  # If it's a single dictionary
            cleaned_row.append(parsed_data)
    except (ValueError, SyntaxError):
        pass  # Skip invalid rows
    return cleaned_row

# Preprocess the column
filtered_df['parsed_tags'] = filtered_df[column_name].apply(preprocess_nested_column)

# Step 2: Extract unique keys from the parsed dictionaries
def extract_keys_from_nested_column(column):
    """
    Extracts unique keys from lists of dictionaries in a column.
    Args:
        column (pd.Series): The input column with lists of dictionaries.
    Returns:
        set: A set of unique keys.
    """
    keys = set()
    for row in column:
        for dictionary in row:
            if isinstance(dictionary, dict):  # Ensure it's a dictionary
                keys.update(dictionary.keys())  # Add the keys to the set
    return keys

unique_keys = extract_keys_from_nested_column(filtered_df['parsed_tags'])

# Step 3: Create one-hot encoded columns for each key
for key in unique_keys:
    filtered_df[f"{column_name}_{key}"] = filtered_df['parsed_tags'].apply(
        lambda x: 1 if any(key in dictionary for dictionary in x if isinstance(dictionary, dict)) else 0
    )

# Drop the intermediate parsed column if no longer needed
filtered_df = filtered_df.drop(columns=['parsed_tags'])

# Display the resulting DataFrame
print(filtered_df.head())
