import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Create an Excel Workbook
wb = Workbook()
ws = wb.active
ws.title = "Styled Tables"

# Define starting row
start_row = 1

# Iterate over all 12 styled DataFrames
for i in range(1, 13):
    styled_df = globals()[f"styled_df_transposed{i}"]  # Get the styled DataFrame

    # Write Caption (Extracted from .style)
    caption = styled_df.export().split("<caption>")[1].split("</caption>")[0]  # Extract caption text
    ws.append([caption])
    start_row += 1  # Move to the next row for the table

    # Convert Styled DataFrame to Excel (preserving existing styles)
    df = styled_df.data  # Extract raw DataFrame

    # Write DataFrame to Excel
    for row in dataframe_to_rows(df, index=True, header=True):
        ws.append(row)

    start_row += len(df) + 2  # Leave space before the next table

# Save the Excel file
wb.save("styled_output.xlsx")
