def generate_timelines(df, customer_col, date_col, annotation_cols, title_col=None):
    """
    Generate compact and readable event timelines for each customer.

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

        # Calculate time deltas and format as HH:MM:SS.000000
        time_deltas = [None] + [
            (group[date_col].iloc[i] - group[date_col].iloc[i - 1])
            for i in range(1, len(group))
        ]
        group["time_delta"] = time_deltas

        # Fixed figure width and height
        min_date = group[date_col].min()
        max_date = group[date_col].max()
        time_range_days = (max_date - min_date).days + 1
        figure_width = max(10, min(20, time_range_days))
        figure_height = 4  # Compact height for visualization

        # Extend the timeline
        extended_start = min_date - pd.Timedelta(days=1)
        extended_end = max_date + pd.Timedelta(days=1)

        # Create figure
        fig, ax = plt.subplots(figsize=(figure_width, figure_height))
        title = f"Timeline for Customer {customer_id}"
        if title_col and title_col in group.columns:
            title += f" ({group[title_col].iloc[0]})"
        ax.set_title(title, pad=20)

        # Add horizontal line above the title
        fig.add_artist(Line2D([0, 1], [1.02, 1.02], color="black", linewidth=1.5, transform=fig.transFigure))

        # Plot timeline
        ax.hlines(y=0, xmin=extended_start, xmax=extended_end, color="black", linewidth=1)
        ax.scatter(group[date_col], [0] * len(group), color="black", zorder=2)

        # Use compact level pattern
        level_pattern = [0.4, -0.4, 0.8, -0.8, 1.2, -1.2]  # Compact levels
        levels = [level_pattern[i % len(level_pattern)] for i in range(len(group))]

        # Add annotations and vertical connector lines
        for i, row in group.iterrows():
            annotation_text = "\n".join([f"{col}: {row[col]}" for col in annotation_cols])
            if row["time_delta"] is not None:
                annotation_text += f"\nTime Delta: {row['time_delta']}"

            # Add vertical connector line
            ax.vlines(x=row[date_col], ymin=0, ymax=levels[i], color="blue", linestyle="--", linewidth=0.8)

            # Add annotation text
            ax.text(
                row[date_col],
                levels[i],
                annotation_text,
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightyellow"),
                fontsize=8,
            )

        # Set x-axis range
        ax.set_xlim(extended_start, extended_end)

        # Dynamically adjust y-axis range
        max_level = max(abs(level) for level in levels)
        ax.set_ylim(-max_level - 0.5, max_level + 0.5)

        # Format x-axis
        ax.set_xticks(group[date_col])
        ax.set_xticklabels(group[date_col].dt.strftime("%Y-%m-%d %H:%M:%S"), rotation=45, ha="right")

        # Hide unnecessary spines and y-axis
        ax.get_yaxis().set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        # Adjust layout to fit annotations
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.3)

        # Display the plot
        plt.show()
