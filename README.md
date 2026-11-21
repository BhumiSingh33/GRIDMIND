GridMind AI 
GridMind AI – AI-Powered Smart Solar Energy Management and Optimization System is a machine learning-based software project designed to manage solar energy efficiently.

The main aim of this project is to make intelligent decisions about how solar-generated electricity should be used, stored, sold, or purchased from the electricity grid.

The system considers seven important inputs: solar power generation, electricity demand, battery level, current electricity price, future electricity price, solar forecast, and time. Based on these inputs, a Random Forest machine learning model predicts the most suitable energy strategy: USE, STORE, SELL, or BUY.

After prediction, a separate optimization module calculates the possible distribution of electricity in kilowatts (kW). The results are displayed through an interactive dashboard developed using Streamlit and Plotly, allowing users to change input values and analyse different energy scenarios.

The project uses Python, Pandas, NumPy, Scikit-learn, Joblib, Streamlit, and Plotly. The model achieved 94% accuracy on the simulated test dataset.

GridMind AI aims to demonstrate how artificial intelligence and optimization techniques can support smarter solar energy management. Currently, it is a software prototype based on simulated data, with real solar hardware integration planned as future work.
Main Features
- AI-based energy strategy prediction.
- Solar generation and electricity demand analysis.
- Battery-level monitoring through user inputs.
- Electricity price and solar forecast consideration.
- Power allocation using an optimization module.
- Interactive dashboard with visual results.
- Testing of different energy scenarios.
