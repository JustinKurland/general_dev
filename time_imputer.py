import pandas as pd
from datetime import timedelta

def impute_missing_values(df, time_col, customer_col, time_window, columns_to_impute):
    """
    Imputes missing values in specified columns based on values from the same customer
    within a specified time window.

    Args:
        df (pd.DataFrame): The input DataFrame.
        time_col (str): Name of the timestamp column.
        customer_col (str): Name of the customer column.
        time_window (timedelta): Time window for finding non-missing values.
        columns_to_impute (list): List of columns to impute.

    Returns:
        pd.DataFrame: DataFrame with missing values imputed.
    """
    # Ensure the time column is a datetime type
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Sort the data by customer and time for efficient processing
    df = df.sort_values(by=[customer_col, time_col])
    
    # Function to fill missing values for a single customer
    def fill_for_customer(customer_data):
        for col in columns_to_impute:
            for i, row in customer_data.iterrows():
                if pd.isna(row[col]):
                    # Find rows within the time window
                    mask = (customer_data[time_col] >= row[time_col] - time_window) & \
                           (customer_data[time_col] <= row[time_col] + time_window)
                    potential_values = customer_data.loc[mask, col].dropna()
                    if not potential_values.empty:
                        # Use the first non-missing value within the time window
                        customer_data.at[i, col] = potential_values.iloc[0]
        return customer_data
    
    # Apply the function to each customer group
    df = df.groupby(customer_col).apply(fill_for_customer)
    
    return df.reset_index(drop=True)


# Load your data into a pandas DataFrame
# df = pd.read_csv("your_data.csv")

# Load your data into a pandas DataFrame
# df = pd.read_csv("your_data.csv")

# Specify the parameters
time_col = "time"
customer_col = "values(customer)"
time_window = timedelta(minutes=10)  # 10-minute time window
columns_to_impute = ["values(TMX_device_id)", "values(TMX_device_id_confidence)", 
                     "values(TMX_device_match_result)"] # Removed 'values(TMX_device_result)'

# Impute missing values
df_imputed = impute_missing_values(toy_df, time_col, customer_col, time_window, columns_to_impute)

# Save or inspect the output
# df_imputed.to_csv("imputed_data.csv", index=False)


import pandas as pd
from datetime import datetime, timedelta

# Create toy data
toy_data = {
    "time": [
        datetime(2024, 12, 10, 8, 0, 0) + timedelta(minutes=i) for i in range(20)
    ],
    "values(customer)": ["cust1"] * 10 + ["cust2"] * 10,
    "values(TMX_device_id)": [None, "id1", None, "id1", None, None, "id1", None, "id1", None] +
                              [None, "id2", None, "id2", None, None, "id2", None, None, "id2"],
    "values(TMX_device_id_confidence)": [100, None, 100, None, None, 100, None, 100, None, None] +
                                        [100, None, 100, None, None, 100, None, 100, None, None],
    "values(TMX_device_match_result)": ["new_device", None, "new_device", None, None, "new_device", None, "new_device", None, None] +
                                       [None, "old_device", None, "old_device", None, None, "old_device", None, None, "old_device"]
}

# Convert to DataFrame
toy_df = pd.DataFrame(toy_data)

# Shuffle rows to simulate realistic unsorted data
toy_df = toy_df.sample(frac=1).reset_index(drop=True)

print(toy_df)
