
from pathlib import Path

import pandas as pd
import streamlit as st

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR

TRAFFIC_FILE = DATA_DIR / "traffic_data.csv"
ACCIDENT_FILE = DATA_DIR / "accidents.csv"

st.set_page_config(
    page_title="Smart City Traffic Analytics",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Smart City Traffic Analytics")
st.write("Traffic monitoring and accident analysis dashboard")

# Load datasets
if not TRAFFIC_FILE.exists() or not ACCIDENT_FILE.exists():
    st.error("Dataset files not found inside the data folder.")
    st.stop()

traffic = pd.read_csv(TRAFFIC_FILE)
accidents = pd.read_csv(ACCIDENT_FILE)

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Traffic Records", f"{len(traffic):,}")
col2.metric("Accident Records", f"{len(accidents):,}")

if "severity" in accidents.columns:
    high_count = int(
        (accidents["severity"] == "High").sum()
    )
else:
    high_count = 0

col3.metric("High-Severity Accidents", high_count)

st.divider()

# Traffic analysis
st.subheader("📊 Traffic Volume Analysis")

if {"timestamp", "traffic_volume"}.issubset(traffic.columns):
    traffic["timestamp"] = pd.to_datetime(
        traffic["timestamp"], errors="coerce"
    )
    traffic = traffic.dropna(subset=["timestamp"])

    traffic["hour"] = traffic["timestamp"].dt.hour

    hourly = traffic.groupby("hour")["traffic_volume"].mean()

    st.bar_chart(hourly)
    st.caption("Average recorded traffic volume by hour.")
else:
    st.warning("Required traffic columns are missing.")

# Accident analysis
st.subheader("🚨 Accidents by Road")

if "road" in accidents.columns:
    road_counts = accidents["road"].value_counts()
    st.bar_chart(road_counts)
else:
    st.warning("The road column was not found.")

# Accident records
st.subheader("📋 Accident Records")
st.dataframe(accidents, use_container_width=True)

# Interactive map link
map_file = DATA_DIR / "outputs" / "accident_risk_map.html"

if map_file.exists():
    st.subheader("🗺️ Accident Risk Map")
    st.success(
        "Your interactive accident map has been generated."
    )
    st.caption(
        "Open data/outputs/accident_risk_map.html "
        "in your browser to view the map."
    )
