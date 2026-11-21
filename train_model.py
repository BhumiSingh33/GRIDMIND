import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("solar_energy_dataset.csv")

print("Dataset loaded successfully!")
print("Total records:", len(df))

# ==========================================
# 2. PREPARE FEATURES
# ==========================================

# Convert forecast_solar into numbers
forecast_encoder = LabelEncoder()

df["forecast_solar"] = forecast_encoder.fit_transform(
    df["forecast_solar"]
)

# Input features
X = df[
    [
        "solar_generation",
        "demand",
        "battery_level",
        "current_price",
        "future_price",
        "forecast_solar",
        "hour"
    ]
]

# Target
y = df["action"]

# Encode target labels
action_encoder = LabelEncoder()
y_encoded = action_encoder.fit_transform(y)

# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print()
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# ==========================================
# 4. RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================
# 5. EVALUATE MODEL
# ==========================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print()
print("======================================")
print("GRIDMIND AI MODEL RESULTS")
print("======================================")
print(f"Accuracy: {accuracy * 100:.2f}%")

print()
print("Classification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=action_encoder.classes_
    )
)

# ==========================================
# 6. SAVE MODEL + ENCODERS
# ==========================================

joblib.dump(model, "gridmind_model.pkl")

joblib.dump(
    forecast_encoder,
    "forecast_encoder.pkl"
)

joblib.dump(
    action_encoder,
    "action_encoder.pkl"
)

print()
print("======================================")
print("Files saved successfully!")
print("======================================")
print("gridmind_model.pkl")
print("forecast_encoder.pkl")
print("action_encoder.pkl")