import requests
import random
import time

API_URL = "https://predictive-maintenance-nxnp.onrender.com/predict"  # Replace with your Render URL

while True:
    data = {
        "temperature": round(random.uniform(70, 100), 3),
        "vibration": round(random.uniform(0.1, 0.5), 3),
        "pressure": round(random.uniform(30, 50), 3),
        "rpm": round(random.uniform(1000, 2000), 3)
    }
    try:
        response = requests.post(API_URL, json=data)
        print(f"Sent: {data}")
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)

    time.sleep(5)  # every 5 seconds
