# Use pandas.merge_asof within groups
matched_dfs = []

for session_id, group_df1 in df1.groupby('sessionID'):
    group_df2 = df2[df2['sessionID'] == session_id]
    if not group_df2.empty:
        # Perform nearest merge_asof for each sessionID group
        matched_group = pd.merge_asof(
            group_df1,
            group_df2,
            on='timestamp',
            direction='nearest',
            suffixes=('_df1', '_df2')
        )
        matched_dfs.append(matched_group)

# Combine all matched groups into a single DataFrame
matched_df = pd.concat(matched_dfs).reset_index(drop=True)

# Display the resulting DataFrame
matched_df
