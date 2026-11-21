import pandas as pd
import joblib

from optimizer import optimize_energy


# ==========================================
# LOAD SAVED MODEL AND ENCODERS
# ==========================================

model = joblib.load("gridmind_model.pkl")
forecast_encoder = joblib.load("forecast_encoder.pkl")
action_encoder = joblib.load("action_encoder.pkl")


# ==========================================
# GRIDMIND PREDICTION FUNCTION
# ==========================================

def predict_energy_strategy(
    solar_generation,
    demand,
    battery_level,
    current_price,
    future_price,
    forecast_solar,
    hour
):

    # Convert forecast into encoded value
    forecast_encoded = forecast_encoder.transform(
        [forecast_solar]
    )[0]

    # Create input dataframe
    input_data = pd.DataFrame({
        "solar_generation": [solar_generation],
        "demand": [demand],
        "battery_level": [battery_level],
        "current_price": [current_price],
        "future_price": [future_price],
        "forecast_solar": [forecast_encoded],
        "hour": [hour]
    })

    # AI prediction
    prediction = model.predict(input_data)[0]

    # Convert prediction back to action
    strategy = action_encoder.inverse_transform(
        [prediction]
    )[0]

    # ======================================
    # OPTIMIZATION
    # ======================================

    allocation = optimize_energy(
        solar_kw=solar_generation,
        demand_kw=demand,
        battery_soc=battery_level,
        strategy=strategy
    )

    return strategy, allocation


# ==========================================
# TEST GRIDMIND
# ==========================================

if __name__ == "__main__":

    strategy, allocation = predict_energy_strategy(
        solar_generation=6,
        demand=2,
        battery_level=50,
        current_price=5,
        future_price=9,
        forecast_solar="High",
        hour=12
    )

    print()
    print("======================================")
    print("       GRIDMIND AI TEST")
    print("======================================")

    print()
    print("INPUT CONDITIONS")
    print("--------------------------------------")
    print("Solar Generation :", 6, "kW")
    print("Demand           :", 2, "kW")
    print("Battery Level    :", 50, "%")
    print("Current Price    : ₹", 5, "/kWh")
    print("Future Price     : ₹", 9, "/kWh")
    print("Solar Forecast   :", "High")
    print("Hour             :", 12)

    print()
    print("AI PREDICTION")
    print("--------------------------------------")
    print("Strategy         :", strategy)

    print()
    print("ENERGY ALLOCATION")
    print("--------------------------------------")
    print("USE              :", allocation["use_kw"], "kW")
    print("STORE            :", allocation["store_kw"], "kW")
    print("SELL             :", allocation["sell_kw"], "kW")
    print("BUY              :", allocation["buy_kw"], "kW")
    print("BATTERY          :", allocation["battery_kw"], "kW")

    print()
    print("======================================")
    print("GridMind AI pipeline working!")
    print("======================================")