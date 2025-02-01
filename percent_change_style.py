import numpy as np

# Compute the month-over-month percentage change (including 'Total')
result_freq_pct_change = result_freq.pct_change() * 100

# Replace NaN and infinite values with '-'
result_freq_pct_change.replace([np.nan, np.inf, -np.inf], '-', inplace=True)

# Apply background gradient styling (on numerical values only)
styled_df = result_freq_pct_change.copy()
numeric_mask = styled_df.applymap(lambda x: isinstance(x, (int, float)))  # Identify numeric values

# Apply gradient only to numeric values
styled_df = styled_df.where(numeric_mask, np.nan)  # Mask non-numeric values for styling
styled_df = styled_df.style.background_gradient(
    cmap="coolwarm", axis=None, vmin=result_freq_pct_change.min().min(), vmax=result_freq_pct_change.max().max()
)

# Format numerical values with percentage sign and ensure placeholders for NaN/Inf
styled_df = styled_df.format(lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else "-")

# Display the styled dataframe
styled_df
