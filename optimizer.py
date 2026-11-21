def optimize_energy(
    solar_kw,
    demand_kw,
    battery_soc,
    strategy,
    max_charge_kw=2.0,
    max_discharge_kw=2.0
):
    """
    GridMind AI - Constraint-Aware Energy Allocation

    Inputs:
        solar_kw       : Current solar generation in kW
        demand_kw      : Current electricity demand in kW
        battery_soc    : Battery state of charge (%)
        strategy       : AI predicted strategy
        max_charge_kw  : Maximum battery charging rate
        max_discharge_kw : Maximum battery discharging rate

    Returns:
        Dictionary containing energy allocation.
    """

    # -----------------------------------------
    # 1. Initialize values
    # -----------------------------------------

    use_kw = 0.0
    store_kw = 0.0
    sell_kw = 0.0
    buy_kw = 0.0
    battery_kw = 0.0

    # -----------------------------------------
    # 2. First use solar for current demand
    # -----------------------------------------

    use_kw = min(solar_kw, demand_kw)

    # Extra solar available
    surplus = max(solar_kw - use_kw, 0)

    # Solar shortage
    deficit = max(demand_kw - use_kw, 0)

    # -----------------------------------------
    # 3. Handle excess solar
    # -----------------------------------------

    if surplus > 0:

        if strategy == "STORE" and battery_soc < 90:

            store_kw = min(
                surplus,
                max_charge_kw
            )

            sell_kw = surplus - store_kw

        elif strategy == "SELL":

            sell_kw = surplus

        else:

            # Default: sell remaining excess
            sell_kw = surplus

    # -----------------------------------------
    # 4. Handle electricity shortage
    # -----------------------------------------

    if deficit > 0:

        if strategy in ["USE", "STORE"] and battery_soc > 20:

            battery_kw = min(
                deficit,
                max_discharge_kw
            )

            buy_kw = deficit - battery_kw

        else:

            buy_kw = deficit

    # -----------------------------------------
    # 5. Return final allocation
    # -----------------------------------------

    return {
        "use_kw": round(use_kw, 2),
        "store_kw": round(store_kw, 2),
        "sell_kw": round(sell_kw, 2),
        "buy_kw": round(buy_kw, 2),
        "battery_kw": round(battery_kw, 2)
    }


# ==========================================
# TEST THE OPTIMIZER
# ==========================================

if __name__ == "__main__":

    result = optimize_energy(
        solar_kw=5,
        demand_kw=2,
        battery_soc=50,
        strategy="STORE"
    )

    print("======================================")
    print("GRIDMIND ENERGY OPTIMIZER TEST")
    print("======================================")

    print("Solar Generation : 5 kW")
    print("Demand           : 2 kW")
    print("Battery Level    : 50%")
    print("AI Strategy      : STORE")

    print()
    print("Energy Allocation:")
    print("----------------------")
    print("USE      :", result["use_kw"], "kW")
    print("STORE    :", result["store_kw"], "kW")
    print("SELL     :", result["sell_kw"], "kW")
    print("BUY      :", result["buy_kw"], "kW")
    print("BATTERY  :", result["battery_kw"], "kW")