import numpy as np
import pandas as pd

def create_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a data dictionary for each column in `df`.
    For each field:
      - Collect its unique values (including NaN).
      - Count the number of unique values.
      - Provide toy text for descriptive columns to be manually updated later.
    Returns a new DataFrame representing this data dictionary.
    """
    data_dict_rows = []

    for col in df.columns:
        # Get unique values (including NaN) for the column
        unique_vals = df[col].fillna(np.nan).unique()
        num_unique = len(unique_vals)

        # Build one row per column with "toy" placeholders
        row = {
            "ColumnName":    col,
            "UniqueValues":  unique_vals.tolist(),  # Convert numpy array to Python list
            "NumUnique":     num_unique,
            "Description":   "This is a toy description to populate later.",
            "Values":        "This is a toy values to populate later.",
            "Example":       "This is a toy example to populate later.",
            "Source":        "This is a toy source to populate later.",
            "Notes":         "This is a toy notes to populate later."
        }

        data_dict_rows.append(row)

    # Convert the list of dictionaries to a DataFrame
    data_dict_df = pd.DataFrame(data_dict_rows)

    # If you have specific “long descriptive” columns (e.g., 'description',
    # 'short_description', 'close_notes', 'u_executive_summary', 'u_work_notes')
    # and want to ensure they appear or have special placeholders, you can
    # optionally handle them here. For example:
    for col_name in ['description','short_description','close_notes','u_executive_summary','u_work_notes']:
        if col_name not in data_dict_df['ColumnName'].values:
            # If the column isn't actually in df, optionally add a row manually:
            data_dict_df = data_dict_df.append(
                {
                    "ColumnName":   col_name,
                    "UniqueValues": [],
                    "NumUnique":    0,
                    "Description":  "This is a toy description to populate later.",
                    "Values":       "This is a toy values to populate later.",
                    "Example":      "This is a toy example to populate later.",
                    "Source":       "This is a toy source to populate later.",
                    "Notes":        "This is a toy notes to populate later."
                },
                ignore_index=True
            )

    # Sort rows by ColumnName if you want a consistent order
    data_dict_df.sort_values(by="ColumnName", inplace=True)

    return data_dict_df


# --------------------------------------------------
# Example usage:
# --------------------------------------------------
if __name__ == "__main__":
    # Let's build a tiny example DataFrame
    data = {
        'category':    ['A', 'B', 'A', 'C', np.nan],
        'priority':    ['high', 'low', 'medium', 'low', 'medium'],
        'some_number': [1, 2, 2, 3, 3],
        'description': ['free text', 'another text', np.nan, 'lorem ipsum', 'dolor sit amet'],
    }
    df_example = pd.DataFrame(data)

    # Create your data dictionary
    data_dict = create_data_dictionary(df_example)

    # Show or export the result
    print(data_dict)
