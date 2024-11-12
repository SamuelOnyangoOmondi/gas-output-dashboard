from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load the pre-trained Random Forest model and anomaly detection model
model = joblib.load('../data/gas_output_model.pkl')
iso_forest = joblib.load('../data/anomaly_detection_model.pkl')

# Define custom thresholds for detecting anomalies
PLASTIC_WASTE_LOWER = 50      # Minimum plastic waste input (kg)
PLASTIC_WASTE_UPPER = 500     # Maximum plastic waste input (kg)
TEMPERATURE_LOWER = 100       # Minimum temperature (Celsius)
TEMPERATURE_UPPER = 400       # Maximum temperature (Celsius)
PRESSURE_LOWER = 50           # Minimum pressure (kPa)
PRESSURE_UPPER = 300          # Maximum pressure (kPa)

# Define a route for the prediction
@app.route('/predict', methods=['POST'])
def predict_gas_output():
    try:
        # Get the data from the request (JSON format)
        data = request.get_json()
        
        # Extract the necessary fields from the request data
        plastic_waste = data.get('Plastic_Waste_Input_kg', None)
        temperature = data.get('Temperature_C', None)
        pressure = data.get('Pressure_kPa', None)

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

        # Run anomaly detection using the Isolation Forest model
        anomaly_flag = iso_forest.predict(input_data)[0]

        # Apply custom rules for detecting anomalies
        custom_anomaly = False
        if not (PLASTIC_WASTE_LOWER <= plastic_waste <= PLASTIC_WASTE_UPPER):
            custom_anomaly = True
        if not (TEMPERATURE_LOWER <= temperature <= TEMPERATURE_UPPER):
            custom_anomaly = True
        if not (PRESSURE_LOWER <= pressure <= PRESSURE_UPPER):
            custom_anomaly = True

        # Combine the results from the model and custom rules
        if anomaly_flag == -1 or custom_anomaly:
            anomaly_status = "Yes"
        else:
            anomaly_status = "No"

        # Return the prediction and anomaly status
        return jsonify({
            'Predicted_Gas_Output_Liters': predicted_gas_output,
            'Anomaly_Flag': anomaly_status
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app (for local testing)
if __name__ == '__main__':
    app.run(debug=True, port=8080)
