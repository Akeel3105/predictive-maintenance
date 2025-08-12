import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")

API_URL = "https://predictive-maintenance-nxnp.onrender.com/recent_predictions"

st.title("📊 Predictive Maintenance Live Dashboard")
placeholder = st.empty()

while True:
    try:
        res = requests.get(API_URL)
        if res.status_code == 200:
            data = res.json().get("data", [])
            if data:
                df = pd.DataFrame(data)
                with placeholder.container():
                    st.dataframe(df)
            else:
                st.write("No predictions yet...")
        else:
            st.error(f"Error fetching data: {res.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

    time.sleep(5)  # Refresh every 5 seconds
