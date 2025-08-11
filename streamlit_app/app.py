# app.py
import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Live Predictions", layout="wide")

API_URL = "https://predictive-maintenance-nxnp.onrender.com/recent_predictions"

st.title("🔴 Real-Time Machine Predictions Dashboard")

placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                placeholder.dataframe(df)
            else:
                st.write("No predictions yet...")
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

    time.sleep(5)  # refresh every 5 seconds
