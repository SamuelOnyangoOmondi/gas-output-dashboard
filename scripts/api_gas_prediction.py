from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Determine the absolute paths based on your current structure
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '../data/gas_output_model.pkl')
anomaly_model_path = os.path.join(current_dir, '../data/anomalies_detected.csv')

# Load the prediction model
model = joblib.load(model_path)

# Load the anomaly detection model (if it's a pre-trained model, otherwise use CSV)
try:
    anomaly_detector = pd.read_csv(anomaly_model_path)
except FileNotFoundError:
    anomaly_detector = None

@app.route('/predict', methods=['POST'])
def predict_gas_output():
    try:
        data = request.get_json()

        # Extract input data
        plastic_waste = data.get('Plastic_Waste_Input_kg')
        temperature = data.get('Temperature_C')
        pressure = data.get('Pressure_kPa')

        if plastic_waste is None or temperature is None or pressure is None:
            return jsonify({'error': 'Missing input data'}), 400

        # Calculate engineered features
        waste_gas_ratio = plastic_waste / 1
        pressure_temp_ratio = pressure / temperature
        waste_pressure_interaction = plastic_waste * pressure

        # Prepare input data for prediction
        input_data = pd.DataFrame({
            'Plastic_Waste_Input_kg': [plastic_waste],
            'Temperature_C': [temperature],
            'Pressure_kPa': [pressure],
            'Waste_Gas_Ratio': [waste_gas_ratio],
            'Pressure_Temp_Ratio': [pressure_temp_ratio],
            'Waste_Pressure_Interaction': [waste_pressure_interaction]
        })

        # Make gas output prediction
        predicted_gas_output = model.predict(input_data)[0]

        # Check for anomalies if anomaly detector is available
        if anomaly_detector is not None:
            is_anomaly = detect_anomaly(input_data)
        else:
            is_anomaly = False

        return jsonify({
            'Predicted_Gas_Output_Liters': predicted_gas_output,
            'Anomaly_Flag': is_anomaly
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def detect_anomaly(input_data):
    """ Simple anomaly detection based on predefined CSV thresholds """
    anomalies = anomaly_detector[
        (anomaly_detector['Plastic_Waste_Input_kg'] == input_data['Plastic_Waste_Input_kg'][0]) &
        (anomaly_detector['Temperature_C'] == input_data['Temperature_C'][0]) &
        (anomaly_detector['Pressure_kPa'] == input_data['Pressure_kPa'][0])
    ]
    return len(anomalies) > 0

if __name__ == '__main__':
    app.run(debug=True, port=8080)
