import streamlit as st
import pandas as pd
import requests
import time

API_URL = "https://predictive-maintenance-nxnp.onrender.com/recent_predictions"  # Replace with your Render URL

st.title("🔴 Predictive Maintenance Live Dashboard")
st.write("Live updates from FastAPI predictions")

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
                st.write("No data yet...")
        else:
            st.write("Error fetching data:", response.status_code)
    except Exception as e:
        st.write("Error:", e)

    time.sleep(5)
