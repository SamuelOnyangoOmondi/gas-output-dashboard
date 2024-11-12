# Import necessary libraries
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import IsolationForest
import joblib

# Dynamically set the correct paths based on the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(BASE_DIR, "../data/plas_tech_gas_data.csv")
model_file_path = os.path.join(BASE_DIR, "../data/gas_output_model.pkl")
anomalies_file_path = os.path.join(BASE_DIR, "../data/anomalies_detected.csv")

# Load the dataset
data = pd.read_csv(data_file_path)

# Features and target variable
features = ['Plastic_Waste_Input_kg', 'Temperature_C', 'Pressure_kPa', 
            'Waste_Gas_Ratio', 'Pressure_Temp_Ratio', 'Waste_Pressure_Interaction']
target = 'Gas_Output_liters'

# Split the data into train and test sets
X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"R-squared: {r2}")

# Save the Random Forest model for future predictions
joblib.dump(rf_model, model_file_path)

# Anomaly Detection using Isolation Forest
iso_forest = IsolationForest(contamination=0.05, random_state=42)
data['Anomaly_Score'] = iso_forest.fit_predict(X)

# Anomalies identified
anomalies = data[data['Anomaly_Score'] == -1]
print(f"Number of anomalies detected: {len(anomalies)}")

# Save anomalies to a CSV file
anomalies.to_csv(anomalies_file_path, index=False)
