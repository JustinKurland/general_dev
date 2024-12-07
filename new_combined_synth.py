# Ensure "Log Likelihood" is numeric
combined_results["Log Likelihood"] = pd.to_numeric(
    combined_results["Log Likelihood"], errors="coerce"
)

# Handle missing or invalid values
if combined_results["Log Likelihood"].isna().sum() > 0:
    print("Warning: Found invalid values in 'Log Likelihood', replacing with default.")
    combined_results["Log Likelihood"].fillna(-1e6, inplace=True)

# Re-run the function
final_conclusion = synthesize_final_conclusion(all_results, combined_results)
print(final_conclusion)
