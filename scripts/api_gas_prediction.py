from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Create a Flask app
app = Flask(__name__)

# Load the trained Random Forest model
model = joblib.load("../data/gas_output_model.pkl")

# Define a route for predicting gas output
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON request data
    data = request.get_json(force=True)
    
    # Extract features from the request data
    plastic_waste_input = data.get('Plastic_Waste_Input_kg')
    temperature_c = data.get('Temperature_C')
    pressure_kpa = data.get('Pressure_kPa')

    # Perform feature engineering (same as what we did during training)
    waste_gas_ratio = plastic_waste_input / 1
    pressure_temp_ratio = pressure_kpa / temperature_c
    waste_pressure_interaction = plastic_waste_input * pressure_kpa

    # Create a DataFrame for the prediction
    input_data = pd.DataFrame({
        'Plastic_Waste_Input_kg': [plastic_waste_input],
        'Temperature_C': [temperature_c],
        'Pressure_kPa': [pressure_kpa],
        'Waste_Gas_Ratio': [waste_gas_ratio],
        'Pressure_Temp_Ratio': [pressure_temp_ratio],
        'Waste_Pressure_Interaction': [waste_pressure_interaction]
    })

    # Predict the gas output using the model
    prediction = model.predict(input_data)[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_Gas_Output_Liters': prediction})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
