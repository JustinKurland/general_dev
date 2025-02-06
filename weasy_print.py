import pandas as pd
from weasyprint import HTML

def save_styled_dataframe_as_image(styled_df, filename="styled_table.png"):
    """Converts a styled Pandas DataFrame to an image while preserving styles using WeasyPrint."""
    
    # Convert styled DataFrame to HTML
    html = styled_df.to_html()

    # Save as an HTML file
    html_filename = "styled_table.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)

    # Convert HTML to PNG using WeasyPrint
    HTML(html_filename).write_png(filename)

# Example usage: Create and style a DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 92, 78]
})

# Apply styling
styled_df = df.style.set_properties(**{
    "background-color": "lightblue",
    "color": "black",
    "border": "1px solid black",
    "text-align": "center"
})

# Save styled DataFrame as an image
save_styled_dataframe_as_image(styled_df, "styled_table.png")
