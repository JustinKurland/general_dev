import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame
# Replace this with your actual DataFrame
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

# Create a plot
customers = df['customer'].unique()
fig, ax = plt.subplots(figsize=(12, 8))

# Loop through each customer to plot their timeline
for i, customer in enumerate(customers):
    customer_data = df[df['customer'] == customer]
    
    # Get unique IPs for y-axis placement
    unique_ips = customer_data['IP'].unique()
    ip_map = {ip: idx for idx, ip in enumerate(unique_ips)}
    
    # Plot each event
    for _, row in customer_data.iterrows():
        ax.plot(row['_time'], ip_map[row['IP']], 'o', label=row['action'])
        ax.text(row['_time'], ip_map[row['IP']], row['action'], fontsize=9, ha='right')
    
    # Add y-axis labels for IPs
    ax.set_yticks(range(len(unique_ips)))
    ax.set_yticklabels(unique_ips)
    
    # Add title and labels
    ax.set_title(f"Timeline of Events for Customer: {customer}")
    ax.set_xlabel("Time")
    ax.set_ylabel("IP Address")
    
    # Show grid for better readability
    ax.grid(True)
    
    # Display the plot for the current customer
    plt.show()
