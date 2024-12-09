The strong disparity in multiple_devices and multiple_IPs between fraud and non-fraud cases is a valuable insight, and you can do more than just compare proportions. Here’s a deeper analysis and modeling approach to make the most of this insight:

1. Analyze the Interaction Between multiple_devices and multiple_IPs

Examine whether the combination of multiple_devices and multiple_IPs creates patterns that differentiate fraud cases more effectively than either feature alone.

a. Cross-Tabulation

Create a cross-tabulation to see how the combination of multiple_devices and multiple_IPs aligns with fraud.

# Create a new feature combining multiple_devices and multiple_IPs
df['multi_device_ip'] = df['multiple_devices'].astype(str) + "_" + df['multiple_IPs'].astype(str)

# Cross-tabulation
cross_tab = pd.crosstab(df['multi_device_ip'], df['target'])
cross_tab['fraud_ratio'] = cross_tab[1] / (cross_tab[0] + cross_tab[1])
print(cross_tab)

# Visualize the fraud ratios for each combination
cross_tab['fraud_ratio'].plot(kind='bar', figsize=(12, 6), title='Fraud Ratio by Multiple Device-IP Combination')
plt.xlabel('Multiple Devices - Multiple IPs')
plt.ylabel('Fraud Ratio')
plt.show()

Interpretation:

	•	Combinations with high fraud ratios may indicate high-risk behavior.
	•	Use these combinations as new categorical features for models.

2. Threshold-Based Analysis

Quantify how the number of devices or IPs affects the likelihood of fraud.

a. Threshold-Based Binning

Bin the number of unique devices and IPs into thresholds and calculate the fraud ratio for each bin.

# Create bins for unique devices and IPs
df['device_bins'] = pd.cut(df['unique_devices'], bins=[0, 1, 2, 5, 10, np.inf], labels=['1', '2', '3-5', '6-10', '10+'])
df['ip_bins'] = pd.cut(df['unique_IPs'], bins=[0, 1, 2, 5, 10, np.inf], labels=['1', '2', '3-5', '6-10', '10+'])

# Calculate fraud ratios for each bin
device_fraud_ratio = df.groupby('device_bins')['target'].mean()
ip_fraud_ratio = df.groupby('ip_bins')['target'].mean()

# Plot fraud ratios
device_fraud_ratio.plot(kind='bar', title='Fraud Ratio by Device Count Bins', figsize=(10, 5))
plt.xlabel('Device Count Bins')
plt.ylabel('Fraud Ratio')
plt.show()

ip_fraud_ratio.plot(kind='bar', title='Fraud Ratio by IP Count Bins', figsize=(10, 5))
plt.xlabel('IP Count Bins')
plt.ylabel('Fraud Ratio')
plt.show()

Interpretation:

	•	Identify thresholds where the likelihood of fraud sharply increases.
	•	Use these thresholds to create new features (e.g., high_risk_device for customers with >5 devices).

3. Temporal Analysis of multiple_devices and multiple_IPs

Investigate whether changes in devices or IPs over time correlate with fraud.

a. Rate of Change

Calculate how frequently devices or IPs change over time.

# Calculate time differences for each customer
df['time_diff'] = df.groupby('customer')['_time'].diff().dt.total_seconds()

# Calculate rates of device/IP changes
df['device_change_rate'] = df.groupby('customer')['device'].transform('nunique') / df.groupby('customer')['time_diff'].transform('sum')
df['ip_change_rate'] = df.groupby('customer')['IP'].transform('nunique') / df.groupby('customer')['time_diff'].transform('sum')

# Compare rates for fraud vs. non-fraud
rate_comparison = df.groupby('target')[['device_change_rate', 'ip_change_rate']].mean()
print(rate_comparison)

Interpretation:

	•	Higher rates of device or IP changes may indicate fraud.
	•	Use these rates as additional features in a model.

4. Network Analysis

Treat device and IP as nodes in a network to uncover relationships between entities.

a. Bipartite Graph

Create a bipartite graph with customers, devices, and IPs to identify fraud-prone connections.

import networkx as nx

# Create a bipartite graph
B = nx.Graph()

# Add nodes for customers, devices, and IPs
B.add_nodes_from(df['customer'].unique(), bipartite=0)  # Customers
B.add_nodes_from(df['device'].unique(), bipartite=1)    # Devices
B.add_nodes_from(df['IP'].unique(), bipartite=1)        # IPs

# Add edges
for _, row in df.iterrows():
    B.add_edge(row['customer'], row['device'])
    B.add_edge(row['customer'], row['IP'])

# Project to customer space
customer_graph = nx.bipartite.projected_graph(B, df['customer'].unique())

# Analyze centrality (fraud-prone customers may have higher centrality)
centrality = nx.degree_centrality(customer_graph)
df['centrality'] = df['customer'].map(centrality)
print(df.groupby('target')['centrality'].mean())

Interpretation:

	•	Customers with higher centrality may have connections to many devices or IPs, indicating potential fraud.
	•	Use centrality as a new feature for fraud detection.

5. Machine Learning with Interaction Terms

Combine these insights into a predictive model by creating interaction terms and engineered features.

a. Create New Features

# Interaction terms
df['devices_ips_interaction'] = df['unique_devices'] * df['unique_IPs']
df['high_risk_combination'] = ((df['unique_devices'] > 3) & (df['unique_IPs'] > 3)).astype(int)

# Train a Random Forest model
X = df[['unique_devices', 'unique_IPs', 'devices_ips_interaction', 'high_risk_combination']]
y = df['target']

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Feature Importance
importances = model.feature_importances_
print(pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False))

6. Anomaly Detection with High-Risk Behavior

Focus on outliers within multiple_devices and multiple_IPs.

a. Isolation Forest

from sklearn.ensemble import IsolationForest

# Fit Isolation Forest
iso = IsolationForest(contamination=0.1, random_state=42)
df['anomaly_score'] = iso.fit_predict(X)

# Compare fraud vs. non-fraud among anomalies
print(df.groupby(['target', 'anomaly_score']).size())

Interpretation:

	•	Fraud cases classified as anomalies confirm that behavior involving multiple devices or IPs is unusual and high-risk.

By exploring these deeper analyses:

	•	You’ll uncover high-risk behaviors in how devices and IPs interact with fraud.
	•	Insights like interaction terms, change rates, and network centrality will help you build more precise models and rules to detect fraud effectively. Let me know if you’d like a specific implementation!
