import json

# Preprocess the column to parse strings into dictionaries
def preprocess_column(column):
    cleaned_data = []
    for row in column.dropna():
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
        cleaned_data.append(cleaned_row)
    return cleaned_data

# Step 1: Preprocess the column
filtered_df[column_name] = preprocess_column(filtered_df[column_name])

# Step 2: Extract all unique keys from the cleaned dictionaries
def extract_keys_from_preprocessed(column):
    keys = set()
    for row in column.dropna():
        for dictionary in row:  # Iterate over parsed dictionaries
            if isinstance(dictionary, dict):  # Ensure it's a dictionary
                keys.update(dictionary.keys())  # Add keys to the set
    return keys

unique_keys = extract_keys_from_preprocessed(filtered_df[column_name])

# Step 3: Create one-hot encoded columns for each key
for key in unique_keys:
    filtered_df[f"{column_name}_{key}"] = filtered_df[column_name].apply(
        lambda x: 1 if any(key in dictionary for dictionary in x if isinstance(dictionary, dict)) else 0
    )

# Display the resulting DataFrame
print(filtered_df)
