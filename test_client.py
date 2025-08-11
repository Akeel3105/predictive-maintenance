# test_client.py
import requests

url = "http://127.0.0.1:8000/predict"

sample_data = {
    "air_temperature": 300.5,
    "process_temperature": 310.0,
    "rotational_speed": 1500,
    "torque": 40
}

response = requests.post(url, json=sample_data)

print("Status Code:", response.status_code)
print("Response:", response.json())
