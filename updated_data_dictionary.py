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
    """
    Create a data dictionary with the following columns:
      - ColumnName
      - Values (all unique values in that column)
      - NumUnique (count of unique values)
      - Example (the first unique value, if any)
      - Description (toy placeholder if column is in SPECIAL_COLS, else None)
      - Source (toy placeholder if column is in SPECIAL_COLS, else None)
      - Notes (toy placeholder if column is in SPECIAL_COLS, else None)
    """
    data_dict_rows = []

    for col in df.columns:
        # Get unique values including NaN
        unique_vals = df[col].fillna(np.nan).unique()
        num_unique = len(unique_vals)
        
        # Pick the first unique value as the "Example" (if it exists)
        example_value = unique_vals[0] if len(unique_vals) > 0 else None

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
            "Values":      unique_vals.tolist(),  # Convert to Python list for readability
            "NumUnique":   num_unique,
            "Example":     example_value,
            "Description": description,
            "Source":      source,
            "Notes":       notes
        }
        data_dict_rows.append(row)

    # Convert the list of dicts into a DataFrame
    data_dict_df = pd.DataFrame(data_dict_rows)

    # Sort by column name if desired
    data_dict_df.sort_values(by="ColumnName", inplace=True)

    return data_dict_df


def update_data_dictionary_value(data_dict: pd.DataFrame, column_name: str,
                                 field_name: str, new_value) -> None:
    """
    Update a single field (e.g. 'Description', 'Source', or 'Notes')
    in the data dictionary for the given 'column_name'.
    This modifies the data_dict DataFrame in-place.
    """
    mask = data_dict['ColumnName'] == column_name
    data_dict.loc[mask, field_name] = new_value


# ---------------------------------------------------------------------
# Example usage:
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Construct a sample DataFrame for demonstration
    df_example = pd.DataFrame({
        'category': ['A', 'B', 'A', 'C', np.nan],
        'priority': ['high', 'low', 'medium', 'low', 'medium'],
        'description': ['some text', 'another text', np.nan, 'lorem ipsum', 'dolor sit amet'],
        'short_description': [np.nan, 'short txt', 'short txt', 'short txt', 'short txt'],
        'random_col': [10, 20, 30, 20, 10]
    })

    # 1) Create the data dictionary
    data_dict = create_data_dictionary(df_example)
    print("Initial Data Dictionary:\n", data_dict, "\n")

    # 2) Suppose later you want to update the 'Source' for 'description'
    update_data_dictionary_value(data_dict, 'description', 'Source', 'Database XYZ')
    #   or update the 'Description' for 'random_col'
    update_data_dictionary_value(data_dict, 'random_col', 'Description',
                                 'This column tracks random values for demonstration.')

    print("After Some Updates:\n", data_dict)
