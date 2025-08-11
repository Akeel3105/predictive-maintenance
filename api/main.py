# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import pandas as pd
from datetime import datetime
import csv

app = FastAPI(title="Predictive Maintenance API")

# Resolve project root and model path (deployment-safe)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "models", "predictive_maintenance_model.pkl")
CSV_FILE = os.path.join(ROOT_DIR, "predictions_log.csv")

# Load model once at startup
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run training first.")
model = joblib.load(MODEL_PATH)

# Pydantic model: must match the feature names used during training
class SensorData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float

@app.get("/")
def root():
    return {"message": "Predictive Maintenance API running"}

@app.post("/predict")
def predict(data: SensorData):
    # Build DataFrame in the same column order used during training
    input_dict = {
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure,
        "rpm": data.rpm
    }
    input_df = pd.DataFrame([input_dict])

    # Prediction
    pred = model.predict(input_df)[0]
    pred_int = int(pred)

    # Prepare CSV log entry
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure,
        "rpm": data.rpm,
        "prediction": pred_int
    }

    # Append to CSV using csv module (safer than reading/writing whole file)
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(log_entry.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

    return {"prediction": pred_int}
