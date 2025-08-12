from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import os

app = FastAPI(title="Predictive Maintenance API")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "predictive_maintenance_model.pkl")
PREDICTIONS_CSV = os.path.join(BASE_DIR, "..", "data", "predictions.csv")

# Make sure data folder exists
os.makedirs(os.path.join(BASE_DIR, "..", "data"), exist_ok=True)

# Load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Expected input schema (MATCH TRAINING FEATURE NAMES)
class MachineData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float

@app.post("/predict")
def predict(data: MachineData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Append to CSV
        record = data.dict()
        record["prediction"] = int(prediction)
        df_out = pd.DataFrame([record])
        if os.path.exists(PREDICTIONS_CSV):
            df_out.to_csv(PREDICTIONS_CSV, mode="a", header=False, index=False)
        else:
            df_out.to_csv(PREDICTIONS_CSV, index=False)

        return {"prediction": int(prediction)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/recent_predictions")
def get_recent_predictions(limit: int = 10):
    if not os.path.exists(PREDICTIONS_CSV):
        return {"data": []}
    df = pd.read_csv(PREDICTIONS_CSV)
    return {"data": df.tail(limit).to_dict(orient="records")}
