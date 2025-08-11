# streamlit_app/app.py
import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Predictive Maintenance - Live Dashboard", layout="wide")
st.title("🔧 Predictive Maintenance — Live Monitoring")

# CSV file path (same as API)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(ROOT_DIR, "predictions_log.csv")

REFRESH_INTERVAL = 5  # seconds

st.markdown("This dashboard reads the live `predictions_log.csv` written by the FastAPI server.")

# Show the latest statistics in a container so they update cleanly
placeholder = st.empty()

def load_and_display():
    if not os.path.exists(CSV_FILE):
        placeholder.warning("No predictions yet. Start the simulator to generate live data.")
        return

    df = pd.read_csv(CSV_FILE)
    # ensure timestamp column is parsed for nicer display
    if "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        except Exception:
            pass

    with placeholder.container():
        st.subheader("📈 Last 20 Predictions")
        st.dataframe(df.tail(20).sort_values(by="timestamp", ascending=False))

        st.subheader("📊 Prediction Counts (last 100)")
        counts = df.tail(100)["prediction"].value_counts().sort_index()
        counts.index = counts.index.astype(str)
        st.bar_chart(counts)

        st.subheader("🧾 Latest Prediction Details")
        st.table(df.tail(1).T)

# Initial load
load_and_display()

# Auto-refresh using simple loop + st.rerun (Streamlit-friendly)
# Note: This will re-run the script every REFRESH_INTERVAL seconds.
time.sleep(REFRESH_INTERVAL)
st.rerun()  # for older versions use st.rerun(); this works in recent versions
