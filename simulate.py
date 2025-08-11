import pandas as pd
import numpy as np
import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "sensor_data.csv")

# Ensure 'data' folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Number of samples
n_samples = 1000

# Simulate sensor readings
np.random.seed(42)  # reproducibility
temperature = np.random.normal(loc=75, scale=10, size=n_samples)  # °C
vibration = np.random.normal(loc=0.5, scale=0.2, size=n_samples)  # mm/s
pressure = np.random.normal(loc=30, scale=5, size=n_samples)      # bar
rpm = np.random.normal(loc=1500, scale=200, size=n_samples)       # rotations/min

# Define failure probability based on abnormal readings
failure_prob = (
    (temperature > 85).astype(int) +
    (vibration > 0.8).astype(int) +
    (pressure < 25).astype(int) +
    (rpm > 1700).astype(int)
)

# Label as 1 (failure risk) if 2+ parameters abnormal
failure = (failure_prob >= 2).astype(int)

# Create DataFrame
df = pd.DataFrame({
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "rpm": rpm,
    "failure": failure
})

# Save dataset
df.to_csv(DATA_PATH, index=False)
print(f"✅ Sensor data saved to {DATA_PATH}")
print(df.head())
