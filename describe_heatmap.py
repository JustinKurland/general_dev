# Generate the descriptive statistics
ohe_stats_percentage = ohe_features.describe()

# Convert numerical statistics (excluding 'count') to percentages
for row in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']:
    if row in ohe_stats_percentage.index:
        ohe_stats_percentage.loc[row] *= 100

# Apply heatmap styling
def heatmap_style(data, cmap="coolwarm"):
    """
    Apply a heatmap to the DataFrame values and then convert to string percentages.
    """
    # Apply heatmap
    styled = data.style.background_gradient(cmap=cmap, axis=None)

    # Convert to percentage strings
    styled = styled.format("{:.2f}%")
    
    return styled

# Apply the heatmap and convert to percentages with strings
styled_df = heatmap_style(ohe_stats_percentage)

# Display the styled DataFrame (in Jupyter Notebook)
styled_df
