Absolutely! Creating cumulative counts for these features will help track patterns over time for each customer. Here’s how you can implement this:

Step 1: Create Cumulative Counts

a. Prepare Data

Ensure that the data is sorted by _time and grouped by customer before calculating cumulative counts.

# Ensure the data is sorted by customer and time
df = df.sort_values(by=['customer', '_time'])

b. Cumulative Count for Unique Logins

Count unique logins cumulatively for each customer.

# Cumulative count of unique logins
df['cumulative_logins'] = df.groupby('customer').cumcount() + 1

c. Cumulative Count for Unique IPs

Track unique IPs cumulatively for each customer.

# Cumulative unique IPs
df['unique_IPs_cumulative'] = df.groupby('customer')['IP'].apply(lambda x: x.expanding().apply(lambda y: len(set(y))))

d. Cumulative Count for Devices

Count unique devices cumulatively. Since you’ve already one-hot encoded the device column, use the browser and mobile_app columns.

# Cumulative counts for device types
df['browser_cumulative'] = df.groupby('customer')['browser'].cumsum()
df['mobile_app_cumulative'] = df.groupby('customer')['mobile_app'].cumsum()

e. Cumulative Count for Actions

Use the one-hot encoded action columns to track cumulative counts for each action type.

# Cumulative counts for each action
actions = ['Login with creds', 'Biometric login', 'Incorrect Password',
           'Failed token refresh', 'Login with OTP', 'OTP prompt', 'OTP initiated without Prompt']

# Assuming actions have already been one-hot encoded, sum each action cumulatively
for action in actions:
    ohe_col = action.replace(" ", "_").lower()  # Adjust the column name to match your OHE columns
    df[f'{ohe_col}_cumulative'] = df.groupby('customer')[ohe_col].cumsum()

Step 2: Verify the Results

Once the columns are created, inspect the results to ensure correctness.

# Display a sample of the cumulative counts
print(df[['customer', '_time', 'cumulative_logins', 'unique_IPs_cumulative', 'browser_cumulative', 'mobile_app_cumulative'] + 
          [f'{action.replace(" ", "_").lower()}_cumulative' for action in actions]].head(10))

Optional: Plot the Cumulative Trends

Visualize how these cumulative counts evolve for specific customers.

a. Plot Cumulative Logins

import matplotlib.pyplot as plt

# Select a specific customer
customer_id = 'example_customer_id'
customer_data = df[df['customer'] == customer_id]

# Plot cumulative logins
plt.figure(figsize=(10, 5))
plt.plot(customer_data['_time'], customer_data['cumulative_logins'], label='Cumulative Logins')
plt.plot(customer_data['_time'], customer_data['unique_IPs_cumulative'], label='Unique IPs')
plt.title(f'Cumulative Counts for Customer {customer_id}')
plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()

b. Plot Device and Action Trends

# Plot cumulative counts for device and actions
plt.figure(figsize=(10, 5))
plt.plot(customer_data['_time'], customer_data['browser_cumulative'], label='Browser Logins')
plt.plot(customer_data['_time'], customer_data['mobile_app_cumulative'], label='Mobile App Logins')
for action in actions:
    plt.plot(customer_data['_time'], customer_data[f'{action.replace(" ", "_").lower()}_cumulative'], label=f'{action} Cumulative')

plt.title(f'Cumulative Device and Action Counts for Customer {customer_id}')
plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()

Step 3: Next Steps

	1.	Aggregate Trends:
	•	Summarize cumulative counts across customers to identify trends (e.g., average number of unique IPs after N logins).
	2.	Feature Engineering:
	•	Use these cumulative counts as features for fraud detection models. For example:
	•	Ratio of unique IPs to cumulative logins.
	•	Ratio of browser to mobile app logins.
	3.	Anomaly Detection:
	•	Identify customers with unusually high counts of Incorrect Password or Failed token refresh relative to their logins.

Let me know if you need additional help with this!
