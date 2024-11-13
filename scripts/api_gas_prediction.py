from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import joblib
import os
import io

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
PLASTIC_WASTE_LOWER = 50      # Minimum plastic waste input (kg)
PLASTIC_WASTE_UPPER = 500     # Maximum plastic waste input (kg)
TEMPERATURE_LOWER = 100       # Minimum temperature (Celsius)
TEMPERATURE_UPPER = 400       # Maximum temperature (Celsius)
PRESSURE_LOWER = 50           # Minimum pressure (kPa)
PRESSURE_UPPER = 300          # Maximum pressure (kPa)

# Helper function to detect anomalies
def detect_anomalies(row):
    """Function to detect anomalies based on predefined thresholds."""
    custom_anomaly = False
    if not (PLASTIC_WASTE_LOWER <= row['Plastic_Waste_Input_kg'] <= PLASTIC_WASTE_UPPER):
        custom_anomaly = True
    if not (TEMPERATURE_LOWER <= row['Temperature_C'] <= TEMPERATURE_UPPER):
        custom_anomaly = True
    if not (PRESSURE_LOWER <= row['Pressure_kPa'] <= PRESSURE_UPPER):
        custom_anomaly = True
    return custom_anomaly

# Route to handle single prediction
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
        custom_anomaly = detect_anomalies(input_data.iloc[0])
        anomaly_status = "Yes" if custom_anomaly else "No"

        return jsonify({
            'Predicted_Gas_Output_Liters': predicted_gas_output,
            'Anomaly_Flag': anomaly_status
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle dataset upload and bulk prediction
@app.route('/upload', methods=['POST'])
def upload_and_predict():
    if model is None:
        return jsonify({'error': 'Model file not found. Please check deployment.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty file uploaded'}), 400

    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Ensure the required columns are present
    required_columns = ['Plastic_Waste_Input_kg', 'Temperature_C', 'Pressure_kPa']
    if not all(col in df.columns for col in required_columns):
        return jsonify({'error': 'Missing required columns'}), 400

    # Calculate features for predictions
    df['Waste_Gas_Ratio'] = df['Plastic_Waste_Input_kg'] / 1
    df['Pressure_Temp_Ratio'] = df['Pressure_kPa'] / df['Temperature_C']
    df['Waste_Pressure_Interaction'] = df['Plastic_Waste_Input_kg'] * df['Pressure_kPa']

    # Make predictions
    features = ['Plastic_Waste_Input_kg', 'Temperature_C', 'Pressure_kPa',
                'Waste_Gas_Ratio', 'Pressure_Temp_Ratio', 'Waste_Pressure_Interaction']
    df['Predicted_Gas_Output_Liters'] = model.predict(df[features])

    # Detect anomalies for each row
    df['Anomaly_Flag'] = df.apply(detect_anomalies, axis=1).apply(lambda x: 'Yes' if x else 'No')

    # Convert the DataFrame to a CSV for download
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='predictions_with_anomalies.csv'
    )

# Run the app (for local testing)
if __name__ == '__main__':
    app.run(debug=True, port=8080)
