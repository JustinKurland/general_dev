import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame
data = {
    "_time": ["2024-12-01 10:00:00", "2024-12-01 10:30:00", "2024-12-01 11:00:00",
              "2024-12-02 10:00:00", "2024-12-02 11:00:00"],
    "customer": ["Alice", "Alice", "Alice", "Bob", "Bob"],
    "IP": ["192.168.1.1", "192.168.1.2", "192.168.1.1", "10.0.0.1", "10.0.0.2"],
    "device": ["laptop", "phone", "tablet", "laptop", "tablet"],
    "action": ["login", "browse", "logout", "login", "logout"]
}

df = pd.DataFrame(data)

# Convert _time to datetime
df['_time'] = pd.to_datetime(df['_time'])

# Sort by time for better visualization
df = df.sort_values(by=['customer', '_time'])

# Create the plot
customers = df['customer'].unique()
fig, axes = plt.subplots(len(customers), 1, figsize=(12, 6 * len(customers)), sharex=True)

if len(customers) == 1:  # If there's only one customer, `axes` won't be an array
    axes = [axes]

for ax, customer in zip(axes, customers):
    customer_data = df[df['customer'] == customer]
    
    # Map unique IPs to y-axis positions
    unique_ips = customer_data['IP'].unique()
    ip_map = {ip: idx for idx, ip in enumerate(unique_ips)}
    
    # Plot each event
    for _, row in customer_data.iterrows():
        ax.plot(row['_time'], ip_map[row['IP']], 'o', label=row['action'], markersize=8)
        ax.text(row['_time'], ip_map[row['IP']], row['action'], fontsize=9, ha='left')
    
    # Set labels and titles
    ax.set_title(f"Timeline of Events for Customer: {customer}", fontsize=14)
    ax.set_yticks(range(len(unique_ips)))
    ax.set_yticklabels(unique_ips)
    ax.set_ylabel("IP Address")
    ax.grid(True)

# Shared X-axis label
plt.xlabel("Time", fontsize=14)
plt.tight_layout()
plt.show()
