import pandas as pd

# Example DataFrame with the 'action' column
data = {
    'action': [
        'Incorrect password|Login with creds',
        'Failed token refresh',
        'Biometric login',
        'OTP prompt|OTP initiated|Login with OTP',
        'OTP initiated without prompt',
        'Incorrect password',
        'OTP prompt',
        'Failed token refresh|OTP prompt',
        'OTP prompt|OTP initiated',
    ]
}

df = pd.DataFrame(data)

# Step 1: Extract all unique individual actions
# Split nested actions and extract unique values
all_actions = set(
    action.strip()
    for actions in df['action'].dropna().str.split('|').tolist()
    for action in actions
)

# Step 2: Create columns for each action and one-hot encode
for action in all_actions:
    df[action] = df['action'].apply(lambda x: 1 if action in str(x).split('|') else 0)

# Display the resulting DataFrame
print(df)
