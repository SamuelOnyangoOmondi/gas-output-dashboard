# Gas Output Prediction Dashboard

This project provides a comprehensive dashboard for monitoring gas output predictions, detecting anomalies, and visualizing gas production data based on input variables such as plastic waste input, temperature, and pressure. The dashboard is designed for use in a waste-to-energy project, where it serves as a tool for assessing gas production performance and identifying irregularities in real-time.

## Demo Video

Watch the demo video of the app here: [Gas Output Prediction Dashboard Demo](https://drive.google.com/file/d/1RLojR5M22UKKP0pvUVrOVYfDvdOyKuYI/view?usp=sharing)

## Deployed Application

Explore the live deployed version of the app on Streamlit: [Gas Output Prediction Dashboard](https://samuelonyangoomondi-gas-output-dash-scriptsgas-dashboard-7vg08h.streamlit.app/)

---

## Features

- **Gas Output Prediction**: Predicts gas output based on user inputs (plastic waste input, temperature, and pressure).
- **Anomaly Detection**: Highlights anomalies in gas production, which can help in troubleshooting operational issues.
- **Data Visualization**: Displays visual trends in gas output over time, allowing users to track performance effectively.
- **Correlation Analysis**: Provides insights into how different variables are correlated.

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

- Python 3.8+
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
3. View predictions, anomaly detections, and interactive visualizations.

---

## Related Files

- **`data/plas_tech_gas_data.csv`**: Main dataset used for training and analysis.
- **`data/gas_output_model.pkl`**: Trained Random Forest model used for predictions.
- **`scripts/gas_dashboard.py`**: Main dashboard script.
- **`scripts/train_gas_output_model.py`**: Script for training the gas output prediction model.
- **`requirements.txt`**: Dependencies required to run the project.

---

## Testing

### Testing Results

- **Functionality Demonstration**: The app successfully predicts gas output and detects anomalies. Screenshots and the demo video (see [Demo Video](#demo-video)) illustrate core functionalities.
- **Testing with Different Data Values**: Tested with varying inputs for plastic waste, temperature, and pressure to verify consistent and realistic outputs.
- **Performance on Different Environments**: 
  - **Streamlit Deployment**: Deployed and tested on Streamlit cloud environment for responsiveness.
  - **Local Environment**: Tested on a Windows machine with Python 3.12. The dashboard functions as expected with minor layout adjustments on mobile screens.

---

## Analysis

The project successfully meets the objectives outlined in the project proposal:
- **Gas Output Prediction**: The model achieves a high accuracy with an R-squared value of 0.98, demonstrating its effectiveness in predicting gas output based on inputs.
- **Anomaly Detection**: Anomalies are correctly flagged using Isolation Forest, helping to identify outliers in gas production.
- **Visualization and Usability**: The interactive dashboard layout improves user experience, enabling easy exploration of data and trends.

---

## Discussion

This project emphasizes the importance of:
- **Predictive Analytics**: Forecasting gas output based on operational variables can help in decision-making and optimizing input levels.
- **Anomaly Detection**: Identifying anomalies ensures operational reliability by alerting users to potential issues early.
- **Visual Insights**: Data visualization enables stakeholders to interpret and act on complex data intuitively.

The milestones achieved (deployment, anomaly detection, and prediction) demonstrate how technology can improve waste-to-energy project management.

---

## Recommendations

1. **Future Enhancements**: Integrate mobile-friendly designs to improve usability on smaller screens.
2. **Scalability**: Consider adding a backend database for storing historical data, enhancing scalability and real-time monitoring.
3. **Community Application**: Waste-to-energy organizations and researchers can use this application to monitor and optimize gas production.

---

## Submission Instructions

1. **Attempt 1**:
   - Submit this GitHub repository containing:
     - This README file.
     - Related project files.
     - Link to the demo video ([Gas Output Prediction Dashboard Demo](https://drive.google.com/file/d/1RLojR5M22UKKP0pvUVrOVYfDvdOyKuYI/view?usp=sharing)).
     - Link to the deployed app ([Streamlit Deployment](https://samuelonyangoomondi-gas-output-dash-scriptsgas-dashboard-7vg08h.streamlit.app/)).

2. **Attempt 2**:
   - Submit a zip file of this repository as submitted in Attempt 1.
