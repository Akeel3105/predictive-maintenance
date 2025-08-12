from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from datetime import datetime

app = FastAPI()

# ===== Load model =====
MODEL_PATH = "predictive_maintenance_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# ===== CSV for storing predictions =====
PREDICTIONS_FILE = "predictions.csv"
if not os.path.exists(PREDICTIONS_FILE):
    pd.DataFrame(columns=["timestamp", "temperature", "vibration", "pressure", "rpm", "prediction"]).to_csv(PREDICTIONS_FILE, index=False)

# ===== Request schema =====
class SensorData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float

# ===== Prediction endpoint =====
@app.post("/predict")
def predict(data: SensorData):
    try:
        # Prepare input
        features = [[data.temperature, data.vibration, data.pressure, data.rpm]]

        # Predict
        prediction = int(model.predict(features)[0])

        # Save to CSV
        df = pd.DataFrame([{
            "timestamp": datetime.now().isoformat(),
            "temperature": data.temperature,
            "vibration": data.vibration,
            "pressure": data.pressure,
            "rpm": data.rpm,
            "prediction": prediction
        }])
        df.to_csv(PREDICTIONS_FILE, mode="a", header=False, index=False)

        return {"prediction": prediction}

    except Exception as e:
        return {"error": str(e)}

# ===== Recent predictions endpoint =====
@app.get("/recent_predictions")
def recent_predictions():
    if os.path.exists(PREDICTIONS_FILE):
        df = pd.read_csv(PREDICTIONS_FILE)
        return df.tail(10).to_dict(orient="records")
    return []

# ===== Root endpoint =====
@app.get("/")
def root():
    return {"message": "Predictive Maintenance API is running"}
