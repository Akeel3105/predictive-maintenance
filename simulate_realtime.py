import requests
import time
import random

API_URL = "https://predictive-maintenance-nxnp.onrender.com/predict"  # Your Render API endpoint

while True:
    payload = {
        "temperature": round(random.uniform(70, 100), 3),
        "vibration": round(random.uniform(0.1, 1.0), 3),
        "pressure": round(random.uniform(20, 50), 3),
        "rpm": round(random.uniform(1000, 2000), 3)
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Sent: {payload}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(3)
