# Select only columns that are binary (contain only 1s and 0s)
binary_columns = filtered_df.columns[
    filtered_df.apply(lambda col: col.isin([0, 1]).all())
]

# Create a new DataFrame with only binary columns
binary_df = filtered_df[binary_columns]

# Display the resulting DataFrame
print(binary_df.head())


# Import necessary libraries
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Step 1: Check for perfectly correlated columns
def drop_perfectly_correlated_columns(df):
    """
    Identifies and drops perfectly correlated columns from the DataFrame.
    """
    # Compute the correlation matrix
    corr_matrix = df.corr()

    # Find columns that are perfectly correlated (correlation = 1.0)
    to_drop = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if corr_matrix.iloc[i, j] == 1.0:  # Perfect correlation
                to_drop.add(corr_matrix.columns[i])
    return df.drop(columns=list(to_drop))

# Apply the function to remove perfectly correlated features
filtered_df = drop_perfectly_correlated_columns(filtered_df)

# Step 2: Ensure data is binary (only 1s and 0s)
# Check if the DataFrame contains only 1s and 0s
binary_check = (filtered_df.isin([0, 1])).all().all()
if not binary_check:
    raise ValueError("The DataFrame contains non-binary values. Please binarize the data first.")

# Step 3: Apply Association Rule Mining
frequent_itemsets = apriori(filtered_df, min_support=0.1, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

# Display the rules
print(rules)


from mlxtend.frequent_patterns import fpgrowth
frequent_itemsets = fpgrowth(filtered_df, min_support=0.1, use_colnames=True)

print(frequent_itemsets)


print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

