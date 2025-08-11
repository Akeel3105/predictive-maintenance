# simulate_realtime.py (place at project root)
import requests
import random
import time

API_URL = "http://127.0.0.1:8000/predict"  # make sure FastAPI is running

def generate_sample():
    return {
        # Use the exact feature names the model expects
        "temperature": round(random.uniform(60, 100), 3),   # °C
        "vibration": round(random.uniform(0.2, 1.5), 3),    # mm/s
        "pressure": round(random.uniform(20, 40), 3),       # bar
        "rpm": round(random.uniform(1000, 2000), 3)         # rpm
    }

def main():
    while True:
        payload = generate_sample()
        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            # If FastAPI returned non-JSON, this will raise and be printed
            response.raise_for_status()
            print("Sent:", payload)
            print("Response:", response.json())
        except Exception as e:
            print("Error:", e)
        time.sleep(2)  # send every 2 seconds (adjust as needed)

if __name__ == "__main__":
    main()
