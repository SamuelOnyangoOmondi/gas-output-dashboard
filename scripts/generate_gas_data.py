import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate the dataset
def generate_gas_data(num_records=1000):
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_records):
        timestamp = start_date + timedelta(hours=i)
        plastic_waste_input = round(random.uniform(50, 500), 2)  # in kg
        gas_output = round(random.uniform(30, 400), 2)  # in liters
        temperature = round(random.uniform(100, 500), 2)  # in Celsius
        pressure = round(random.uniform(50, 300), 2)  # in kPa
        anomaly_flag = random.choices([0, 1], weights=[95, 5])[0]  # 5% chance of anomaly
        
        # Feature engineering
        waste_gas_ratio = plastic_waste_input / gas_output if gas_output != 0 else 0
        pressure_temp_ratio = pressure / temperature if temperature != 0 else 0
        waste_pressure_interaction = plastic_waste_input * pressure

        # Add to dataset
        data.append([plastic_waste_input, gas_output, temperature, pressure, anomaly_flag,
                     timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                     waste_gas_ratio, pressure_temp_ratio, waste_pressure_interaction])

    columns = ['Plastic_Waste_Input_kg', 'Gas_Output_liters', 'Temperature_C', 'Pressure_kPa', 'Anomaly_Flag',
               'Year', 'Month', 'Day', 'Hour', 'Waste_Gas_Ratio', 'Pressure_Temp_Ratio', 'Waste_Pressure_Interaction']
    
    return pd.DataFrame(data, columns=columns)

# Generate the dataset
gas_data = generate_gas_data()

# Save to CSV (under data folder)
gas_data.to_csv("../data/plas_tech_gas_data.csv", index=False)

print("Dataset generated and saved as 'plas_tech_gas_data.csv' in the data folder.")
