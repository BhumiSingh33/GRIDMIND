import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 1000

data = {
    'voltage': np.random.uniform(210, 250, n_samples),
    'current': np.random.uniform(5, 50, n_samples),
    'temperature': np.random.uniform(15, 45, n_samples),
    'humidity': np.random.uniform(30, 90, n_samples),
    'grid_load': np.random.uniform(100, 500, n_samples)
}

df = pd.DataFrame(data)
df['power'] = df['voltage'] * df['current']
df['status'] = np.where((df['temperature'] > 38) & (df['grid_load'] > 400), 1, 0)

df.to_csv('grid_data.csv', index=False)
print('Dataset successfully generated: grid_data.csv')
