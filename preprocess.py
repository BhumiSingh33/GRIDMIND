import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv('grid_data.csv')
print('--- Dataset Info ---')
print(df.info())
print('\n--- Target Distribution ---')
print(df['status'].value_counts())

# Separate Features (X) and Target (y)
X = df.drop('status', axis=1)
y = df['status']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print('\nPreprocessing successful!')
print(f'Train shape: {X_train_scaled.shape}, Test shape: {X_test_scaled.shape}')
