import json

# Preprocess the column to parse strings into dictionaries
def preprocess_column(row):
    """
    Parses each row in the column, cleaning and converting items into dictionaries.
    Args:
        row (str): The input row string.
    Returns:
        list: A list of parsed dictionaries or an empty list if invalid.
    """
    if pd.isna(row):
        return []  # Return empty list for NaN values

    cleaned_row = []
    for item in row.split(','):  # Split by commas
        try:
            # Replace single quotes with double quotes and strip whitespace
            cleaned_item = item.strip().replace("'", '"')
            # Parse as a dictionary
            parsed_dict = json.loads(cleaned_item)
            cleaned_row.append(parsed_dict)
        except json.JSONDecodeError:
            pass  # Skip invalid entries
    return cleaned_row

# Step 1: Apply preprocessing function to each row
filtered_df['parsed_reasons'] = filtered_df[column_name].apply(preprocess_column)

# Step 2: Extract all unique keys from the cleaned dictionaries
def extract_keys_from_preprocessed(column):
    """
    Extracts unique keys from lists of dictionaries in the column.
    Args:
        column (pd.Series): The input column with lists of dictionaries.
    Returns:
        set: A set of unique keys.
    """
    keys = set()
    for row in column:
        for dictionary in row:  # Iterate over parsed dictionaries
            if isinstance(dictionary, dict):  # Ensure it's a dictionary
                keys.update(dictionary.keys())  # Add keys to the set
    return keys

# Extract unique keys
unique_keys = extract_keys_from_preprocessed(filtered_df['parsed_reasons'])

# Step 3: Create one-hot encoded columns for each key
for key in unique_keys:
    filtered_df[f"{column_name}_{key}"] = filtered_df['parsed_reasons'].apply(
        lambda x: 1 if any(key in dictionary for dictionary in x if isinstance(dictionary, dict)) else 0
    )

# Display the resulting DataFrame
print(filtered_df)
