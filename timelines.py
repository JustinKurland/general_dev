import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def generate_timelines(df, customer_col, date_col, annotation_cols, title_col=None):
    """
    Generates timelines for each customer with flexible annotations.

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
    grouped = df.groupby(customer_col)

    for customer_id, group in grouped:
        # Sort by date
        group = group.sort_values(by=date_col).reset_index(drop=True)
        dates = group[date_col].tolist()

        # Calculate time deltas between events
        time_deltas = [None] + [
            (dates[i] - dates[i - 1]).total_seconds() / 3600 for i in range(1, len(dates))
        ]
        group['Time Delta (hours)'] = time_deltas

        # Generate staggered levels for better visualization
        level_pattern = [3, 5, 7, 5, 3]
        levels = np.tile(level_pattern, int(np.ceil(len(dates) / len(level_pattern))))[: len(dates)]

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        title = f"Event Timeline for Customer {customer_id}"
        if title_col and title_col in group.columns:
            title += f" ({group[title_col].iloc[0]})"
        ax.set_title(title)

        # Plot the timeline
        ax.plot(dates, np.zeros_like(dates), color="black", linewidth=0.5, zorder=1)
        ax.scatter(dates, np.zeros_like(dates), color="black", zorder=2)

        # Annotate each event with a text box
        for i, (date, level, row) in enumerate(zip(dates, levels, group.itertuples())):
            annotation_text = "\n".join(
                [f"{col}: {getattr(row, col)}" for col in annotation_cols]
            )
            if row._10:  # Include time delta if not None
                annotation_text += f"\nTime Delta: {row._10:.2f} hrs"

            ax.text(
                date,
                level,
                annotation_text,
                ha="center",
                va="bottom" if level > 0 else "top",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
                fontsize=9,
            )

        # Format x-axis with date labels
        ax.set_xticks(dates)
        ax.set_xticklabels(
            [d.strftime("%Y-%m-%d %H:%M:%S") for d in dates],
            rotation=45,
            ha="right",
        )

        # Clean up the plot
        ax.get_yaxis().set_visible(False)  # Hide y-axis
        ax.spines["left"].set_visible(False)  # Hide unnecessary spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.tight_layout()

        # Show the timeline
        plt.show()
