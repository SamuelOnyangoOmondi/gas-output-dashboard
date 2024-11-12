from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained Random Forest model
model = joblib.load('../data/gas_output_model.pkl')

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

        # Check for missing inputs
        if plastic_waste is None or temperature is None or pressure is None:
            return jsonify({'error': 'Missing input data'}), 400

        # Calculate engineered features
        waste_gas_ratio = plastic_waste / 1  # Adjust based on actual data
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
        prediction = model.predict(input_data)[0]

        # Return the prediction result as JSON
        return jsonify({'Predicted_Gas_Output_Liters': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app (for local testing)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
