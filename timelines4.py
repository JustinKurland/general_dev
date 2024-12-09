import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

def generate_timelines(df, customer_col, date_col, annotation_cols, title_col=None):
    """
    Generate compact and readable event timelines for each customer with evenly spaced events.

    Parameters:
        df (pd.DataFrame): The input dataset.
        customer_col (str): Column name for customer ID.
        date_col (str): Column name for event timestamps.
        annotation_cols (list of str): Column names to include in event annotations.
        title_col (str, optional): Column name for timeline title (e.g., customer name).
    """
    # Ensure the date column is in datetime format
    df[date_col] = pd.to_datetime(df[date_col])

    # Group by customer ID
    for customer_id, group in df.groupby(customer_col):
        # Sort group by date
        group = group.sort_values(by=date_col).reset_index(drop=True)

        # Calculate time deltas
        time_deltas = [None] + [
            (group[date_col].iloc[i] - group[date_col].iloc[i - 1])
            for i in range(1, len(group))
        ]
        group["time_delta"] = time_deltas

        # Create an evenly spaced x-axis
        x_positions = list(range(len(group)))
        group["x_position"] = x_positions

        # Fixed figure width and height
        figure_width = 12
        figure_height = 6

        # Create figure
        fig, ax = plt.subplots(figsize=(figure_width, figure_height))
        title = f"Timeline for Customer {customer_id}"
        if title_col and title_col in group.columns:
            title += f" ({group[title_col].iloc[0]})"
        ax.set_title(title, pad=30)

        # Add horizontal line above the title
        fig.add_artist(Line2D([0, 1], [1.03, 1.03], color="black", linewidth=1.5, transform=fig.transFigure))

        # Plot timeline with a buffer for aesthetics
        ax.hlines(y=0, xmin=-1, xmax=len(group), color="black", linewidth=1)
        ax.scatter(group["x_position"], [0] * len(group), color="black", zorder=2)

        # Alternate y-positions for annotations
        level_pattern = [1, -1, 2, -2]
        levels = [level_pattern[i % len(level_pattern)] for i in range(len(group))]

        # Add annotations and vertical connector lines
        for i, row in group.iterrows():
            annotation_text = "\n".join([f"{col}: {row[col]}" for col in annotation_cols])
            if row["time_delta"] is not None:
                annotation_text += f"\nTime Delta: {row['time_delta']}"

            # Add vertical connector line
            ax.vlines(x=row["x_position"], ymin=0, ymax=levels[i], color="gray", linestyle="--", linewidth=0.8)

            # Add annotation text (centered)
            ax.text(
                row["x_position"],
                levels[i],
                annotation_text,
                ha="center",  # Centered horizontally
                va="bottom" if levels[i] > 0 else "top",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
                fontsize=8,
            )

        # Set x-axis ticks and labels evenly
        ax.set_xticks(group["x_position"])
        ax.set_xticklabels(group[date_col].dt.strftime("%Y-%m-%d\n%H:%M:%S"), rotation=45, ha="right")

        # Dynamically adjust y-axis range
        max_level = max(abs(level) for level in levels)
        ax.set_ylim(-max_level - 1, max_level + 1)

        # Hide unnecessary spines and y-axis
        ax.get_yaxis().set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        # Adjust layout to fit annotations
        plt.tight_layout()

        # Display the plot
        plt.show()
