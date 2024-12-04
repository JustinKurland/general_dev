# Generate the descriptive statistics
ohe_stats_percentage = ohe_features.describe()

# Convert numerical statistics (excluding 'count') to percentages
for row in ['min', '25%', '50%', '75%', 'max']:
    if row in ohe_stats_percentage.index:
        ohe_stats_percentage.loc[row] *= 100

# Define a function for heatmap styling with conditional formatting
def conditional_heatmap(data, rows_to_style, cmap="coolwarm"):
    """
    Apply heatmap gradient only to specified rows and format numerical values as percentages.
    """
    # Create a Styler object
    styled = data.style

    # Apply gradient only to the specified rows
    for row in rows_to_style:
        if row in data.index:
            styled = styled.background_gradient(
                subset=pd.IndexSlice[row, :], cmap=cmap, axis=1
            )

    # Format numerical values as percentages, excluding count, mean, and std
    styled = styled.format(
        lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else x,
        subset=pd.IndexSlice[rows_to_style, :]
    )

    return styled

# Apply the heatmap with percentage formatting to specific rows
rows_to_style = ['min', '25%', '50%', '75%', 'max']
styled_df = conditional_heatmap(ohe_stats_percentage, rows_to_style)

# Display the styled DataFrame (in Jupyter Notebook or similar environments)
styled_df
