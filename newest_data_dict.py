import pandas as pd
import numpy as np

SPECIAL_COLS = [
    'description',
    'short_description',
    'close_notes',
    'u_executive_summary',
    'u_work_notes'
]

def create_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    data_dict_rows = []

    for col in df.columns:
        # Get all unique values (including NaN)
        unique_vals = df[col].unique()

        # Convert to Python list for readability (including NaN)
        unique_vals_list = unique_vals.tolist()

        # Filter out NaN values to find a better 'Example'
        non_nan_vals = [val for val in unique_vals if pd.notna(val)]
        
        # Count them
        num_unique = len(unique_vals_list)

        # The first non-NaN unique value (if any) as 'Example'
        example_value = non_nan_vals[0] if len(non_nan_vals) > 0 else None

        # If this column is one of the special columns, fill with toy placeholders
        if col in SPECIAL_COLS:
            description = "This is a toy description to populate later."
            source = "This is a toy source to populate later."
            notes = "This is a toy notes to populate later."
        else:
            description = None
            source = None
            notes = None

        row = {
            "ColumnName":  col,
            "Values":      unique_vals_list, 
            "NumUnique":   num_unique,
            "Example":     example_value,
            "Description": description,
            "Source":      source,
            "Notes":       notes
        }
        data_dict_rows.append(row)

    data_dict_df = pd.DataFrame(data_dict_rows)
    # Sort by column name if desired
    data_dict_df.sort_values(by="ColumnName", inplace=True)
    data_dict_df.reset_index(drop=True, inplace=True)
    
    return data_dict_df

# Helper function for updating a single field in the data dictionary
def update_data_dictionary_value(data_dict: pd.DataFrame, column_name: str,
                                 field_name: str, new_value) -> None:
    mask = data_dict['ColumnName'] == column_name
    data_dict.loc[mask, field_name] = new_value


# Example usage
if __name__ == "__main__":
    df_example = pd.DataFrame({
        'category': ['A', 'B', 'A', 'C', np.nan],
        'priority': ['high', 'low', 'medium', 'low', 'medium'],
        'description': ['some text', 'another text', np.nan, 'lorem ipsum', 'dolor sit amet'],
        'short_description': [np.nan, 'short txt', 'short txt', 'short txt', 'short txt'],
        'random_col': [10, 20, 30, 20, 10]
    })

    data_dict = create_data_dictionary(df_example)
    print("Initial Data Dictionary:\n", data_dict, "\n")

    # Example of updating the 'Source' for 'description'
    update_data_dictionary_value(data_dict, 'description', 'Source', 'Database XYZ')
    print("After update:\n", data_dict)
