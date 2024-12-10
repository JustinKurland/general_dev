# Count occurrences of each session ID in the original DataFrame
counts_original = toy_df['values(customer)'].value_counts().rename('count_original')

# Count occurrences of each session ID in the deduplicated DataFrame
counts_deduplicated = deduplicated_df['values(customer)'].value_counts().rename('count_deduplicated')

# Combine the counts into a single DataFrame
counts_comparison = pd.concat([counts_original, counts_deduplicated], axis=1).fillna(0)

# Convert counts to integers
counts_comparison = counts_comparison.astype(int)

# Display the resulting DataFrame
counts_comparison
