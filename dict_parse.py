import pandas as pd
import ast

# Sample DataFrame
data = {
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'col_with_dicts': [
        '{"data1","data2"}',  # Example string representation of a set
        '{"data2","data3"}',
        '{"data1"}',
        None,
        '{"data3","data4"}'
    ]
}
df = pd.DataFrame(data)

# Step 1: Parse strings to actual Python sets, handling None gracefully
def parse_to_set(value):
    if isinstance(value, str):
        # Convert string like '{"data1","data2"}' to Python set
        return set(ast.literal_eval(value.replace("”", '"').replace("“", '"')))
    return set()

df['col_with_dicts'] = df['col_with_dicts'].apply(parse_to_set)

# Step 2: Get all unique strings across the dictionaries
unique_strings = set().union(*df['col_with_dicts'])

# Step 3: Generate one-hot encoded columns
for string in unique_strings:
    df[string] = df['col_with_dicts'].apply(lambda x: 1 if string in x else 0)

# Optional: Drop the original column if no longer needed
# df = df.drop(columns=['col_with_dicts'])

print(df)
