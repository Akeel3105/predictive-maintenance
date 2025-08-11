import joblib
import os
import numpy as np

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "predictive_maintenance_model.pkl")

# Load trained model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found at {MODEL_PATH}. Train the model first.")

model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully!")

def predict_failure(temperature, vibration, pressure, rpm):
    """Predict failure risk based on sensor readings."""
    input_data = np.array([[temperature, vibration, pressure, rpm]])
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        return "⚠️ Failure Risk Detected!"
    else:
        return "✅ Machine is Healthy."

# Example run
if __name__ == "__main__":
    # Example sensor input
    temp = float(input("Enter temperature (°C): "))
    vib = float(input("Enter vibration (mm/s): "))
    pres = float(input("Enter pressure (bar): "))
    rpm_val = float(input("Enter RPM: "))

    result = predict_failure(temp, vib, pres, rpm_val)
    print("\nPrediction Result:", result)
