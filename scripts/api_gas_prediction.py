from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Dynamically set the base directory for absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the pre-trained Random Forest model
model_path = os.path.join(BASE_DIR, '../data/gas_output_model.pkl')

# Load the model with error handling
try:
    model = joblib.load(model_path)
except FileNotFoundError as e:
    print(f"Error loading model: {e}")
    model = None

# Define custom thresholds for detecting anomalies
PLASTIC_WASTE_LOWER = 50
PLASTIC_WASTE_UPPER = 500
TEMPERATURE_LOWER = 100
TEMPERATURE_UPPER = 400
PRESSURE_LOWER = 50
PRESSURE_UPPER = 300

# Helper function to detect anomalies
def detect_anomalies(plastic_waste, temperature, pressure):
    if not (PLASTIC_WASTE_LOWER <= plastic_waste <= PLASTIC_WASTE_UPPER):
        return True
    if not (TEMPERATURE_LOWER <= temperature <= TEMPERATURE_UPPER):
        return True
    if not (PRESSURE_LOWER <= pressure <= PRESSURE_UPPER):
        return True
    return False

# Define a route for the prediction
@app.route('/predict', methods=['POST'])
def predict_gas_output():
    # Check if the model is loaded
    if model is None:
        return jsonify({'error': 'Model file not found. Please check deployment.'}), 500

    try:
        # Get the data from the request (JSON format)
        data = request.get_json()

        # Extract the necessary fields from the request data
        plastic_waste = data.get('Plastic_Waste_Input_kg')
        temperature = data.get('Temperature_C')
        pressure = data.get('Pressure_kPa')

        # Validate input fields
        if plastic_waste is None or temperature is None or pressure is None:
            return jsonify({'error': 'Missing input data'}), 400

        # Calculate engineered features
        waste_gas_ratio = plastic_waste / 1
        pressure_temp_ratio = pressure / temperature
        waste_pressure_interaction = plastic_waste * pressure

        # Prepare the input data for prediction
        input_data = pd.DataFrame({
            'Plastic_Waste_Input_kg': [plastic_waste],
            'Temperature_C': [temperature],
            'Pressure_kPa': [pressure],
            'Waste_Gas_Ratio': [waste_gas_ratio],
            'Pressure_Temp_Ratio': [pressure_temp_ratio],
            'Waste_Pressure_Interaction': [waste_pressure_interaction]
        })

        # Make the prediction
        predicted_gas_output = model.predict(input_data)[0]

        # Detect anomalies
        is_anomaly = detect_anomalies(plastic_waste, temperature, pressure)
        anomaly_status = "Yes" if is_anomaly else "No"

        return jsonify({
            'Predicted_Gas_Output_Liters': predicted_gas_output,
            'Anomaly_Flag': anomaly_status
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app (for local testing)
if __name__ == '__main__':
    app.run(debug=True, port=8080)
