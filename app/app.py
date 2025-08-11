import streamlit as st
import joblib
import os
import numpy as np

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "predictive_maintenance_model.pkl")

# Load model
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model not found at {MODEL_PATH}. Please run model.py first.")
else:
    model = joblib.load(MODEL_PATH)
    st.success("✅ Model loaded successfully!")

# App title
st.title("🛠️ AI-Powered Predictive Maintenance System")
st.write("Enter sensor readings to predict machine health status.")

# Input sliders for sensor data
temperature = st.slider("Temperature (°C)", 50, 120, 75)
vibration = st.slider("Vibration (mm/s)", 0.1, 2.0, 0.5)
pressure = st.slider("Pressure (bar)", 10, 50, 30)
rpm = st.slider("RPM", 500, 3000, 1500)

# Predict button
if st.button("🔍 Predict"):
    if 'model' in locals():
        input_data = np.array([[temperature, vibration, pressure, rpm]])
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("⚠️ Failure Risk Detected! Schedule maintenance soon.")
        else:
            st.success("✅ Machine is Healthy.")
