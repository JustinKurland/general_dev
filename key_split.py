import ast  # To safely evaluate string representations of dictionaries

# Example column name
column_name = 'Reasons'

# Step 1: Extract all unique keys from the dictionaries
# Split rows by ',' and extract keys from each dictionary
def extract_keys(column):
    keys = set()
    for row in column.dropna():
        # Split by ',' and parse each dictionary
        for item in row.split(','):
            try:
                dictionary = ast.literal_eval(item.strip())
                keys.update(dictionary.keys())
            except (ValueError, SyntaxError):
                pass
    return keys

# Get all unique keys
unique_keys = extract_keys(df[column_name])

# Step 2: Create columns for each key and one-hot encode
for key in unique_keys:
    df[f"{column_name}_{key}"] = df[column_name].apply(
        lambda x: 1 if x and any(key in ast.literal_eval(item.strip()) for item in x.split(',')) else 0
    )

# Display the resulting DataFrame
print(df)
