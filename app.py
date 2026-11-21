import streamlit as st
import plotly.graph_objects as go

from predict import predict_energy_strategy


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="GridMind AI",
    page_icon="☀️",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.strategy-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #ddd;
    margin-bottom: 20px;
}

.strategy {
    font-size: 32px;
    font-weight: 700;
}

.metric-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
}

.metric-title {
    font-size: 16px;
    color: #666;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">☀️ GridMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Smart Solar Energy Management & Optimization System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# SIDEBAR - INPUTS
# ==========================================

st.sidebar.header("⚙️ Energy Inputs")

solar_generation = st.sidebar.number_input(
    "☀️ Solar Generation (kW)",
    min_value=0.0,
    max_value=10.0,
    value=6.0,
    step=0.1
)

demand = st.sidebar.number_input(
    "⚡ Energy Demand (kW)",
    min_value=0.0,
    max_value=8.0,
    value=2.0,
    step=0.1
)

battery_level = st.sidebar.slider(
    "🔋 Battery Level (%)",
    min_value=0,
    max_value=100,
    value=50
)

current_price = st.sidebar.number_input(
    "💰 Current Electricity Price (₹/kWh)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.5
)

future_price = st.sidebar.number_input(
    "📈 Future Electricity Price (₹/kWh)",
    min_value=0.0,
    max_value=20.0,
    value=9.0,
    step=0.5
)

forecast_solar = st.sidebar.selectbox(
    "🌤️ Solar Forecast",
    ["Low", "Medium", "High"],
    index=2
)

hour = st.sidebar.slider(
    "🕐 Current Hour",
    min_value=0,
    max_value=23,
    value=12
)


# ==========================================
# ANALYZE BUTTON
# ==========================================

analyze = st.sidebar.button(
    "🚀 Analyze Energy",
    width="stretch"
)


# ==========================================
# DEFAULT / ANALYSIS
# ==========================================

if analyze:

    strategy, allocation = predict_energy_strategy(
        solar_generation=solar_generation,
        demand=demand,
        battery_level=battery_level,
        current_price=current_price,
        future_price=future_price,
        forecast_solar=forecast_solar,
        hour=hour
    )

    # ======================================
    # AI PREDICTION
    # ======================================

    st.subheader("🤖 AI Decision")

    st.markdown(
        f"""
        <div class="strategy-box">
            <div>Recommended Energy Strategy</div>
            <div class="strategy">{strategy}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================
    # INPUT SUMMARY
    # ======================================

    st.subheader("📊 Current Energy Conditions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Solar Generation",
            f"{solar_generation:.1f} kW"
        )

    with col2:
        st.metric(
            "Energy Demand",
            f"{demand:.1f} kW"
        )

    with col3:
        st.metric(
            "Battery Level",
            f"{battery_level}%"
        )

    with col4:
        st.metric(
            "Current Price",
            f"₹{current_price:.1f}/kWh"
        )

    # ======================================
    # ENERGY ALLOCATION
    # ======================================

    st.subheader("⚡ Energy Allocation")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏠 USE",
            f"{allocation['use_kw']:.2f} kW"
        )

    with col2:
        st.metric(
            "🔋 STORE",
            f"{allocation['store_kw']:.2f} kW"
        )

    with col3:
        st.metric(
            "💰 SELL",
            f"{allocation['sell_kw']:.2f} kW"
        )

    with col4:
        st.metric(
            "🛒 BUY",
            f"{allocation['buy_kw']:.2f} kW"
        )

    st.write(
        f"Battery discharge used: "
        f"**{allocation['battery_kw']:.2f} kW**"
    )

    # ======================================
    # VISUALIZATION
    # ======================================

    st.subheader("📈 Energy Distribution")

    labels = [
        "USE",
        "STORE",
        "SELL",
        "BUY"
    ]

    values = [
        allocation["use_kw"],
        allocation["store_kw"],
        allocation["sell_kw"],
        allocation["buy_kw"]
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                text=[f"{v:.2f} kW" for v in values],
                textposition="auto"
            )
        ]
    )

    fig.update_layout(
        title="GridMind AI Energy Allocation",
        xaxis_title="Energy Action",
        yaxis_title="Power (kW)",
        height=450
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ======================================
    # DECISION EXPLANATION
    # ======================================

    st.subheader("🧠 Decision Explanation")

    if strategy == "STORE":
        st.info(
            "GridMind AI recommends STORE because surplus solar "
            "energy can be stored in the battery for future use."
        )

    elif strategy == "SELL":
        st.info(
            "GridMind AI recommends SELL because available surplus "
            "solar energy can be exported to the grid."
        )

    elif strategy == "USE":
        st.info(
            "GridMind AI recommends USE because available solar "
            "energy is suitable for meeting current demand."
        )

    elif strategy == "BUY":
        st.info(
            "GridMind AI recommends BUY because current solar and "
            "battery availability are not sufficient to meet demand."
        )

    # ======================================
    # SYSTEM FLOW
    # ======================================

    st.subheader("🔄 GridMind AI Decision Pipeline")

    st.markdown("""
    **Solar + Demand + Battery + Price + Forecast**

    ↓

    **Random Forest AI**

    ↓

    **USE / STORE / SELL / BUY**

    ↓

    **Constraint-Aware Energy Optimizer**

    ↓

    **Exact Energy Allocation**
    """)

else:

    # ======================================
    # WELCOME SCREEN
    # ======================================

    st.info(
        "👈 Enter the current energy conditions from the sidebar "
        "and click **Analyze Energy** to run GridMind AI."
    )

    st.subheader("🌱 What does GridMind AI do?")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### ☀️")
        st.write("Monitors solar generation")

    with col2:
        st.markdown("### ⚡")
        st.write("Analyzes energy demand")

    with col3:
        st.markdown("### 🔋")
        st.write("Considers battery status")

    with col4:
        st.markdown("### 🤖")
        st.write("Predicts the best energy strategy")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "GridMind AI | AI-powered solar energy management prototype | "
    "Currently using simulated dataset"
)