import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Create the main figure
fig, ax = plt.subplots(figsize=(12, 6))

# Create a Basemap instance with only land boundaries
m = Basemap(projection="cyl", llcrnrlat=-60, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180, ax=ax)

# Draw landmasses only
m.drawmapboundary(fill_color="white")
m.fillcontinents(color="lightgrey", lake_color="white")

# Define unique colors for each region
region_colors = {"AMERICAS": "blue", "APAC": "green", "EMEA": "orange"}

# Adjusted inset plot size for better visibility
inset_width, inset_height = 0.14, 0.08

# Finalized positions for the inset plots
region_inset_positions = {
    "AMERICAS": (0.25, 0.50),  # Perfectly positioned
    "APAC": (0.68, 0.40),  # Perfectly positioned
    "EMEA": (0.49, 0.62)  # Perfectly positioned
}

# Add a subplot at each regional centroid for the time series plots
for region, (x_pos, y_pos) in region_inset_positions.items():
    # Create inset axes for the time series plot with translucent background
    ax_inset = fig.add_axes([x_pos, y_pos, inset_width, inset_height], facecolor="none", alpha=0.7)

    # Plot the time series for the region with small markers
    ax_inset.plot(df.index, df[region], marker="o", markersize=2, linestyle="-", color=region_colors[region])

    # Format the inset plot with small x and y-axis labels, but no axis titles
    ax_inset.set_xticks(df.index[::3])  # Show every third month
    ax_inset.set_xticklabels(df.index[::3], rotation=45, fontsize=5)
    ax_inset.set_yticks([df[region].min(), df[region].max()])  # Show min and max count values
    ax_inset.set_yticklabels([df[region].min(), df[region].max()], fontsize=5)  # Label y-axis values

    # Set the title with a transparent background and black font
    ax_inset.set_title(region, fontsize=7, pad=2, backgroundcolor="none", color="black")

    # Remove unnecessary borders and axis labels
    ax_inset.spines["top"].set_visible(False)
    ax_inset.spines["right"].set_visible(False)
    ax_inset.set_xlabel("")  # Remove x-axis title
    ax_inset.set_ylabel("")  # Remove y-axis title

# Adjust layout and show
plt.show()


import pandas as pd

# Create the DataFrame
data = {
    'AMERICAS': [21, 29, 30, 35, 28, 51, 57, 98, 92, 70, 71, 64],
    'APAC': [3, 7, 8, 12, 17, 17, 21, 29, 34, 28, 36, 25],
    'EMEA': [8, 7, 5, 7, 15, 18, 16, 28, 34, 38, 38, 29]
}

# Define the months as the index
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Construct the DataFrame
df = pd.DataFrame(data, index=months)

# Display the DataFrame
print(df)
