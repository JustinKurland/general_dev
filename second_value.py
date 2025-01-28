def make_second_char_white(val):
    """Styles the second character of a column name in white (invisible)."""
    if len(val) > 1:
        return f'color: white'
    return ''

# Define a dictionary of styles
column_styles = [
    {"selector": f"th.col_heading.level0:nth-child({i+1})",
     "props": [("color", "white")]} if len(col) > 1 else {}
    for i, col in enumerate(df_transposed.columns)
]

# Apply styling
styled_df_transposed = df_transposed.style.background_gradient(
    cmap=custom_cmap, axis=None, vmin=result_freq.min().min(), vmax=result_freq.max().max()
).set_table_styles(column_styles)
