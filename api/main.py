# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# Load model
with open("models/predictive_maintenance_model.pkl", "rb") as f:
    model = pickle.load(f)

PREDICTIONS_FILE = "predictions.csv"

class MachineData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float

@app.post("/predict")
def predict(data: MachineData):
    features = [[data.temperature, data.vibration, data.pressure, data.rpm]]
    prediction = model.predict(features)[0]

    # Append to CSV
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure,
        "rpm": data.rpm,
        "prediction": prediction
    }

    if not os.path.exists(PREDICTIONS_FILE):
        pd.DataFrame([record]).to_csv(PREDICTIONS_FILE, index=False)
    else:
        df = pd.read_csv(PREDICTIONS_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        df.to_csv(PREDICTIONS_FILE, index=False)

    return {"prediction": int(prediction)}

@app.get("/recent_predictions")
def recent_predictions(limit: int = 10):
    if not os.path.exists(PREDICTIONS_FILE):
        return []
    df = pd.read_csv(PREDICTIONS_FILE)
    return df.tail(limit).to_dict(orient="records")
