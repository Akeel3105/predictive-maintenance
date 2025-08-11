# api/model.py
import joblib
import os

def load_model():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(ROOT_DIR, "models", "predictive_maintenance_model.pkl")
    return joblib.load(MODEL_PATH)
