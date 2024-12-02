import pandas as pd
import matplotlib.pyplot as plt

# Sample dataframe (replace this with your actual dataframe)
# df = pd.read_csv("your_file.csv")  # Load your dataframe here

# Sum the counts for each category
category_totals = df[['text', 'tables', 'diagrams/figures', 'images', 'code']].sum()

# Create the plot
plt.figure(figsize=(10, 6))
category_totals.plot(kind='bar', color='skyblue', edgecolor='black')

# Add labels and title
plt.title('Distribution of Categories', fontsize=16)
plt.xlabel('Categories', fontsize=14)
plt.ylabel('Total Count', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Sample dataframe (replace this with your actual dataframe)
# df = pd.read_csv("your_file.csv")  # Load your dataframe here

# Create a column that represents combinations of categories
df['combination'] = df[['text', 'tables', 'diagrams/figures', 'images', 'code']].apply(
    lambda row: ', '.join(row.index[row > 0]), axis=1
)

# Count the occurrences of each combination
combination_counts = df['combination'].value_counts()

# Plot the distribution of combinations
plt.figure(figsize=(12, 8))
combination_counts.plot(kind='bar', color='lightcoral', edgecolor='black')

# Add labels and title
plt.title('Distribution of Category Combinations', fontsize=16)
plt.xlabel('Category Combinations', fontsize=14)
plt.ylabel('Number of Articles', fontsize=14)
plt.xticks(rotation=45, fontsize=10, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()


# Count the number of modalities used in each article
df['num_modalities'] = df[['text', 'tables', 'diagrams/figures', 'images', 'code']].gt(0).sum(axis=1)

# Calculate the distribution of modality counts
modality_distribution = df['num_modalities'].value_counts().sort_index()

# Plot the distribution
plt.figure(figsize=(8, 6))
modality_distribution.plot(kind='bar', color='steelblue', edgecolor='black')

plt.title('Distribution of Modalities Per Article', fontsize=16)
plt.xlabel('Number of Modalities', fontsize=14)
plt.ylabel('Number of Articles', fontsize=14)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

import seaborn as sns

# Create a co-occurrence matrix
co_occurrence = df[['text', 'tables', 'diagrams/figures', 'images', 'code']].T.dot(
    df[['text', 'tables', 'diagrams/figures', 'images', 'code']]
)

# Plot the co-occurrence matrix
plt.figure(figsize=(8, 6))
sns.heatmap(co_occurrence, annot=True, fmt='d', cmap='Blues', cbar=True)

plt.title('Co-Occurrence Matrix of Modalities', fontsize=16)
plt.xlabel('Modalities', fontsize=14)
plt.ylabel('Modalities', fontsize=14)
plt.tight_layout()
plt.show()

# Mock example: Assume you have a column mapping articles to ATT&CK techniques
df['techniques'] = ['Execution', 'Persistence', 'Initial Access', ...]  # Example data

# Count occurrences of techniques per modality
modality_impact = df[['text', 'tables', 'diagrams/figures', 'images', 'code']].T.dot(
    pd.get_dummies(df['techniques'])
)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(modality_impact, annot=True, cmap='Reds', cbar=True, fmt='d')

plt.title('Impact of Modalities on MITRE ATT&CK Techniques', fontsize=16)
plt.xlabel('MITRE ATT&CK Techniques', fontsize=14)
plt.ylabel('Modalities', fontsize=14)
plt.tight_layout()
plt.show()


