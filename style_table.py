from matplotlib.colors import LinearSegmentedColormap

start_date = '2024-02-01'
end_date = '2025-01-31'
freq = 'M'

df = convert_opened_at_datetime(df)
df = replace_u_impacted_regionnew_values(df)
df = u_impacted_regionnew_ohe(df)

# Compute frequencies
result_freq = sum_one_hot_encoded_with_frequency(df, start_date, end_date, 'opened_at', freq)
result_freq.rename_axis(None, inplace=True)

# Convert index to first letter of the month, ensuring uniqueness
month_abbr = result_freq.index.strftime('%b')[0]  # Keep only the first letter

# Ensure uniqueness by appending indices if duplicates exist
unique_months = []
counts = {}

for m in month_abbr:
    if m in counts:
        counts[m] += 1
        unique_months.append(f"{m}{counts[m]}")  # Make "J" -> "J1", "J2", etc.
    else:
        counts[m] = 1
        unique_months.append(m)

result_freq.index = unique_months  # Assign the unique month abbreviations

# Apply styling with custom colormap
colors = ['#ffffff', '#2f3b5c']
n_bins = 100
cmap_name = 'custom_cmap'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

styled_df = result_freq.style.background_gradient(
    cmap=custom_cmap, axis=None, vmin=result_freq.min().min(), vmax=result_freq.max().max()
)

# Transpose DataFrame
df_transposed = result_freq.T

# Rename columns with unique month names after transposing
df_transposed.columns = unique_months  

# Apply styling again after renaming
styled_df_transposed = df_transposed.style.background_gradient(
    cmap=custom_cmap, axis=None, vmin=result_freq.min().min(), vmax=result_freq.max().max()
)

styled_df_transposed
