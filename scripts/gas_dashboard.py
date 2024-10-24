import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load the dataset
data = pd.read_csv("data/plas_tech_gas_data.csv")  # Updated path

# Load the saved Random Forest model
rf_model = joblib.load("data/gas_output_model.pkl")  # Updated path

# Filter anomalies based on the Anomaly_Flag
anomalies = data[data['Anomaly_Flag'] == 1]

# Set up the Streamlit app layout with better visuals
st.markdown('<p class="title-font">🌟 Gas Output Prediction Dashboard</p>', unsafe_allow_html=True)
st.markdown("### Monitor gas output, anomalies, and predict gas output with enhanced visuals!")

# Display key metrics with improved layout
st.write(f"""
    <div class="metrics-container">
        <div class="metric-box">
            <h4>Total Data Records</h4>
            <p class="big-num">{len(data)}</p>
        </div>
        <div class="metric-box">
            <h4>Total Anomalies Detected</h4>
            <p class="big-num">{len(anomalies)}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add a section for Gas Output Prediction
st.markdown('<p class="section-title">🔮 Predict Gas Output</p>', unsafe_allow_html=True)

# Create input fields for user input with padding and background color
waste_input = st.number_input("Plastic Waste Input (kg)", min_value=50.0, max_value=500.0, value=100.0)
temperature_input = st.number_input("Temperature (Celsius)", min_value=100.0, max_value=500.0, value=300.0)
pressure_input = st.number_input("Pressure (kPa)", min_value=50.0, max_value=300.0, value=150.0)

# Calculate engineered features
waste_gas_ratio = waste_input / 1  # Adjust this based on real data
pressure_temp_ratio = pressure_input / temperature_input
waste_pressure_interaction = waste_input * pressure_input

# Create a dataframe for the prediction
input_data = pd.DataFrame({
    'Plastic_Waste_Input_kg': [waste_input],
    'Temperature_C': [temperature_input],
    'Pressure_kPa': [pressure_input],
    'Waste_Gas_Ratio': [waste_gas_ratio],
    'Pressure_Temp_Ratio': [pressure_temp_ratio],
    'Waste_Pressure_Interaction': [waste_pressure_interaction]
})

# Predict the gas output based on user input
predicted_gas_output = rf_model.predict(input_data)

# Display the prediction result with an icon
st.markdown(f"""
    <div class="prediction-result">
        <h4>🌍 Predicted Gas Output</h4>
        <p class="big-num">{predicted_gas_output[0]:.2f} Liters</p>
    </div>
    """, unsafe_allow_html=True)

# Add checkbox to filter data to show only anomalies
show_anomalies = st.checkbox("Show Only Anomalies")

if show_anomalies:
    filtered_data = anomalies
else:
    filtered_data = data

# Visualize Gas Output over time
st.markdown('<p class="section-title">📈 Gas Output Over Time</p>', unsafe_allow_html=True)
fig = px.line(filtered_data, x='Day', y='Gas_Output_liters', title='Gas Output Over Time', markers=True)

# Customize chart visuals
fig.update_layout({
    'plot_bgcolor': 'rgba(255, 255, 255, 1)',
    'paper_bgcolor': 'rgba(255, 255, 255, 1)',
    'font': {'size': 14},
})

# Highlight anomalies in the chart with a different color
if show_anomalies:
    fig.update_traces(marker=dict(color='red'))
st.plotly_chart(fig)

# Display filtered data with a polished table
st.markdown('<p class="section-title">📊 Data with Anomalies Highlighted</p>', unsafe_allow_html=True)
st.dataframe(filtered_data)

# Add correlation heatmap
st.markdown('<p class="section-title">📊 Correlation Heatmap Between Features</p>', unsafe_allow_html=True)
corr_matrix = data[['Plastic_Waste_Input_kg', 'Gas_Output_liters', 'Temperature_C', 'Pressure_kPa']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Add CSS for better styling
st.markdown("""
    <style>
    .title-font {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    .section-title {
        font-size: 22px;
        font-weight: bold;
        padding-top: 20px;
    }
    .metrics-container {
        display: flex;
        justify-content: space-evenly;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        width: 30%;
    }
    .big-num {
        font-size: 32px;
        font-weight: bold;
        color: #0099ff;
    }
    .prediction-result {
        background-color: #e3f2fd;
        border-left: 5px solid #0099ff;
        padding: 20px;
        margin-top: 20px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
