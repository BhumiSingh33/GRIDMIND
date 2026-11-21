import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Solar Dataset
df = pd.read_csv('solar_energy_dataset.csv')

# Encode Categorical Column (forecast_solar: Low=0, Medium=1, High=2)
le = LabelEncoder()
df['forecast_solar'] = le.fit_transform(df['forecast_solar'])

# Features and Target
X = df.drop('action', axis=1)
y = df['action']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest Training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluation
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print('======================================')
print('GridMind Solar Model Training Results')
print('======================================')
print(f'Model Accuracy: {accuracy * 100:.2f}%')
print('\nClassification Report:')
print(classification_report(y_test, y_pred))

# Save Model, Scaler, and Label Encoder
joblib.dump(model, 'solar_model.pkl')
joblib.dump(scaler, 'solar_scaler.pkl')
joblib.dump(le, 'solar_encoder.pkl')
print('\nSaved artifacts: solar_model.pkl, solar_scaler.pkl, solar_encoder.pkl')
