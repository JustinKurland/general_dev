# Get the unique session IDs in the original DataFrame
unique_sessions_original = set(toy_df['values(customer)'].unique())

# Get the unique session IDs in the deduplicated DataFrame
unique_sessions_deduplicated = set(deduplicated_df['values(customer)'].unique())

# Find the difference between the two sets
sessions_only_in_original = unique_sessions_original - unique_sessions_deduplicated
sessions_only_in_deduplicated = unique_sessions_deduplicated - unique_sessions_original

# Print results
print(f"Unique session IDs in original DataFrame: {len(unique_sessions_original)}")
print(f"Unique session IDs in deduplicated DataFrame: {len(unique_sessions_deduplicated)}")
print(f"Session IDs only in original: {sessions_only_in_original}")
print(f"Session IDs only in deduplicated: {sessions_only_in_deduplicated}")
