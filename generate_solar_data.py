import pandas as pd
import numpy as np

np.random.seed(42)

# Number of records
n_samples = 5000

# Generate realistic solar energy conditions
solar_generation = np.random.uniform(0, 10, n_samples)
demand = np.random.uniform(1, 8, n_samples)
battery_level = np.random.uniform(10, 100, n_samples)

current_price = np.random.uniform(4, 12, n_samples)
future_price = current_price + np.random.uniform(-3, 5, n_samples)

forecast_solar = np.random.choice(
    ["Low", "Medium", "High"],
    n_samples,
    p=[0.30, 0.40, 0.30]
)

hour = np.random.randint(0, 24, n_samples)

# Create DataFrame
df = pd.DataFrame({
    "solar_generation": solar_generation,
    "demand": demand,
    "battery_level": battery_level,
    "current_price": current_price,
    "future_price": future_price,
    "forecast_solar": forecast_solar,
    "hour": hour
})


# --------------------------------------------------
# Create decision labels
# --------------------------------------------------

def decide_action(row):

    solar = row["solar_generation"]
    demand = row["demand"]
    battery = row["battery_level"]
    current_price = row["current_price"]
    future_price = row["future_price"]
    forecast = row["forecast_solar"]

    # If solar is insufficient
    if solar < demand:

        # Battery has enough energy
        if battery > 30:
            return "USE"

        # Battery is low -> buy from grid
        else:
            return "BUY"

    # Solar is greater than demand
    else:

        excess = solar - demand

        # Battery almost full
        if battery >= 90:
            return "SELL"

        # Current price is attractive
        elif current_price > future_price:
            return "SELL"

        # Future price expected to increase
        elif future_price > current_price + 1:
            return "STORE"

        # Good solar forecast and battery has space
        elif forecast == "High" and battery < 80:
            return "STORE"

        else:
            return "SELL"


df["action"] = df.apply(decide_action, axis=1)


# Save dataset
df.to_csv("solar_energy_dataset.csv", index=False)

print("======================================")
print("GridMind Solar Dataset Created!")
print("======================================")
print(f"Total records: {len(df)}")
print()
print("Columns:")
print(df.columns.tolist())
print()
print("Action distribution:")
print(df["action"].value_counts())
print()
print("Dataset saved as:")
print("solar_energy_dataset.csv")