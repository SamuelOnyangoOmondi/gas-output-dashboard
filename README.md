# Gas Output Prediction Dashboard

This project provides a robust and interactive dashboard for **predicting gas output**, detecting anomalies, and visualizing gas production trends using input variables like **plastic waste quantity**, **temperature**, and **pressure**. It was designed for **Plas-Tech's waste-to-energy initiative** to enhance gas production efficiency, reduce waste, and ensure operational safety.

## Demo Video

Watch the demo video showcasing the dashboard's functionalities: [Gas Output Prediction Dashboard Demo](https://drive.google.com/file/d/1RLojR5M22UKKP0pvUVrOVYfDvdOyKuYI/view?usp=sharing)

## Deployed Application

Explore the live deployed version of the dashboard here: [Gas Output Prediction Dashboard](https://www.plastechenergies.com/blank)

---

## Features

- **Gas Output Prediction**: Uses a Random Forest model to predict gas output based on user inputs (plastic waste input, temperature, and pressure).
- **Anomaly Detection**: Utilizes an Isolation Forest model to detect anomalies, helping identify irregularities in gas production.
- **Data Visualization**: Displays interactive graphs to analyze trends in gas output and variable interactions over time.
- **User-Friendly Interface**: Seamlessly integrated with Wix for accessibility and enhanced user interaction.

---

## Table of Contents

- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Related Files](#related-files)
- [Testing](#testing)
- [Analysis](#analysis)
- [Discussion](#discussion)
- [Recommendations](#recommendations)

---

## Installation and Setup

Follow these steps to set up and run the dashboard locally:

### Prerequisites

- Python 3.10+
- Git

### Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SamuelOnyangoOmondi/gas-output-dashboard.git
   cd gas-output-dashboard
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv myenv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install the Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Dashboard**

   ```bash
   streamlit run scripts/gas_dashboard.py
   ```

---

## Usage

1. Open the app in your browser (usually opens automatically after running).
2. Input desired values for:
   - **Plastic Waste Input** (in kg)
   - **Temperature** (in Celsius)
   - **Pressure** (in kPa)
3. The dashboard displays:
   - **Predicted Gas Output**: Estimated gas production based on inputs.
   - **Anomaly Detection**: Alerts if irregularities are detected.
   - **Interactive Visualizations**: Analyze trends over time.

---

## Related Files

- **`data/plas_tech_gas_data.csv`**: Dataset used for training and analysis.
- **`data/gas_output_model.pkl`**: Trained Random Forest model for predictions.
- **`scripts/gas_dashboard.py`**: Main dashboard script.
- **`scripts/train_gas_output_model.py`**: Script for training the prediction model.
- **`scripts/api_gas_prediction.py`**: Flask API for integrating predictions with Wix.
- **`requirements.txt`**: List of required Python packages.

---

## Testing

### Testing Results

- **Model Accuracy**: The Random Forest model achieved an R-squared value of **0.95**, indicating high accuracy in predictions.
- **Anomaly Detection**: Effectively flags anomalies, ensuring safe and efficient operations.
- **Performance on Deployment**: Deployed successfully on Wix and Streamlit, tested for responsiveness and usability across different devices.
  
---

## Analysis

The project's objectives were met successfully:
- **High Accuracy in Predictions**: The model consistently delivers reliable predictions of gas output.
- **Anomaly Detection**: Early detection of anomalies ensures smooth operation and safety.
- **User Interface**: A visually appealing and intuitive dashboard enhances user experience.

---

## Discussion

The project highlights the importance of:
- **Predictive Analytics**: Accurate forecasting of gas output helps optimize input parameters and improve efficiency.
- **Data-Driven Decision Making**: Anomaly detection and interactive visualizations empower users to make informed decisions.
- **Integration with Existing Systems**: Using a Flask API and Wix platform integration ensures smooth operation with minimal overhead.

---

## Recommendations

1. **Future Enhancements**: Expand functionality to include mobile optimization and real-time alerts.
2. **Scalability**: Leverage cloud services for storing historical data, enabling advanced analytics and scalability.
3. **Potential Use Cases**: Waste-to-energy projects, environmental sustainability initiatives, and research in resource optimization.

---

## Submission Instructions

- Submit the following items for evaluation:
  - Updated **GitHub repository**: [Gas Output Prediction Dashboard](https://github.com/SamuelOnyangoOmondi/gas-output-dashboard)
  - Demo video link: [Watch Demo](https://drive.google.com/file/d/1RLojR5M22UKKP0pvUVrOVYfDvdOyKuYI/view?usp=sharing)
  - Link to the **deployed dashboard**: [Wix Deployment](https://www.plastechenergies.com/blank)

---

## License

This project is open-source and available under the [MIT License](LICENSE).

