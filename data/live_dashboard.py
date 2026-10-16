
from pathlib import Path
from datetime import datetime
import html
import uuid

import pandas as pd
import folium
import streamlit as st
from folium.plugins import Fullscreen, HeatMap
from streamlit_folium import st_folium

# --------------------------------------------------
# 1. PROJECT PATHS
# This script is inside the data folder.
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ACCIDENT_FILE = BASE_DIR / "accidents.csv"
LIVE_FILE = BASE_DIR / "live_accidents.csv"
MAP_FILE = OUTPUT_DIR / "live_accident_map.html"

# Approximate default location: Sirsi, Karnataka
DEFAULT_LAT = 14.6200
DEFAULT_LON = 74.8350

st.set_page_config(
    page_title="Smart City Traffic Analytics",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Smart City Traffic Analytics")
st.subheader("Live Accident Detection Demonstration")

st.info(
    "Demonstration mode: accidents triggered using the test button "
    "are simulated events, not automatically detected real crashes."
)


# --------------------------------------------------
# 2. LOAD AND CLEAN DATA
# --------------------------------------------------
def load_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        st.warning(f"Unable to read {path.name}.")
        return pd.DataFrame()


def prepare_accidents(df, source):
    columns = [
        "latitude", "longitude", "severity",
        "road", "timestamp", "source"
    ]

    if df.empty:
        return pd.DataFrame(columns=columns)

    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    aliases = {
        "lat": "latitude",
        "lon": "longitude",
        "lng": "longitude",
        "risk": "severity",
        "date": "timestamp",
        "datetime": "timestamp",
        "time": "timestamp",
        "location": "road"
    }

    df = df.rename(columns=aliases)

    for column in ["latitude", "longitude"]:
        if column not in df.columns:
            df[column] = pd.NA

        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    if "severity" not in df.columns:
        df["severity"] = "Low"

    if "road" not in df.columns:
        df["road"] = "Unknown"

    if "timestamp" not in df.columns:
        df["timestamp"] = "Not available"

    df = df.dropna(
        subset=["latitude", "longitude"]
    ).copy()

    df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ].copy()

    df["severity"] = (
        df["severity"].astype(str).str.strip().str.title()
    )

    df["road"] = df["road"].fillna("Unknown").astype(str)
    df["timestamp"] = (
        df["timestamp"].fillna("Not available").astype(str)
    )
    df["source"] = source

    return df[columns]


# --------------------------------------------------
# 3. SIMULATE AN ACCIDENT
# --------------------------------------------------
st.header("🧪 Test Accident Trigger")

st.write(
    "Enter a location, select severity, and trigger a test event. "
    "The event will be saved and displayed on the map."
)

with st.form("test_accident_form"):
    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "GPS latitude",
            min_value=-90.0,
            max_value=90.0,
            value=DEFAULT_LAT,
            format="%.6f"
        )

        road = st.text_input(
            "Road / location",
            value="Sirsi Demo Road"
        )

    with col2:
        longitude = st.number_input(
            "GPS longitude",
            min_value=-180.0,
            max_value=180.0,
            value=DEFAULT_LON,
            format="%.6f"
        )

        severity = st.selectbox(
            "Accident severity",
            ["High", "Medium", "Low"]
        )

    submitted = st.form_submit_button(
        "🚨 TRIGGER TEST ACCIDENT",
        type="primary",
        width="stretch"
    )

if submitted:
    event = {
        "event_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "road": road.strip() or "Unknown",
        "latitude": latitude,
        "longitude": longitude,
        "severity": severity,
        "source": "Simulated test event"
    }

    try:
        event_df = pd.DataFrame([event])

        event_df.to_csv(
            LIVE_FILE,
            mode="a",
            header=(
                not LIVE_FILE.exists()
                or LIVE_FILE.stat().st_size == 0
            ),
            index=False
        )

        st.session_state["last_test_event"] = event

        st.rerun()

    except OSError as exc:
        st.error(f"Could not save the event: {exc}")


if "last_test_event" in st.session_state:
    event = st.session_state["last_test_event"]

    st.success(
        f"Test event recorded | Severity: {event['severity']} | "
        f"GPS: {event['latitude']:.6f}, "
        f"{event['longitude']:.6f}"
    )


# --------------------------------------------------
# 4. LOAD ALL ACCIDENT RECORDS
# --------------------------------------------------
historical = prepare_accidents(
    load_csv(ACCIDENT_FILE),
    "Existing dataset"
)

live = prepare_accidents(
    load_csv(LIVE_FILE),
    "Simulated test event"
)

all_accidents = pd.concat(
    [historical, live],
    ignore_index=True
)

high_count = int(
    (all_accidents["severity"] == "High").sum()
)

medium_count = int(
    (all_accidents["severity"] == "Medium").sum()
)

low_count = int(
    (all_accidents["severity"] == "Low").sum()
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Historical records", len(historical))
m2.metric("Test events", len(live))
m3.metric("High severity", high_count)
m4.metric("Medium severity", medium_count)


# --------------------------------------------------
# 5. BUILD THE REAL-WORLD STREET MAP
# --------------------------------------------------
st.header("🗺️ Interactive Accident Map")

if all_accidents.empty:
    center = [DEFAULT_LAT, DEFAULT_LON]
    zoom = 13
else:
    # Focus on the newest test event when one is available.
    if not live.empty:
        latest = live.iloc[-1]
        center = [
            float(latest["latitude"]),
            float(latest["longitude"])
        ]
        zoom = 15
    else:
        center = [
            float(all_accidents["latitude"].mean()),
            float(all_accidents["longitude"].mean())
        ]
        zoom = 13

risk_map = folium.Map(
    location=center,
    zoom_start=zoom,
    tiles="OpenStreetMap",
    control_scale=True
)

Fullscreen().add_to(risk_map)

# Heatmap
if not all_accidents.empty:
    heat_layer = folium.FeatureGroup(
        name="Accident Heatmap",
        show=False
    )

    heat_data = all_accidents[
        ["latitude", "longitude"]
    ].values.tolist()

    HeatMap(
        heat_data,
        radius=20,
        blur=15
    ).add_to(heat_layer)

    heat_layer.add_to(risk_map)

# Separate layers
historical_layer = folium.FeatureGroup(
    name="Historical Accident Records",
    show=True
)

live_layer = folium.FeatureGroup(
    name="Simulated Test Accidents",
    show=True
)

colors = {
    "High": "red",
    "Medium": "orange",
    "Low": "green"
}

for _, row in all_accidents.iterrows():
    severity_value = str(row["severity"]).title()
    color = colors.get(severity_value, "blue")

    popup_html = f"""
    <div style="width:250px">
        <h4>Accident Record</h4>
        <b>Road:</b> {html.escape(str(row["road"]))}<br>
        <b>Severity:</b> {html.escape(severity_value)}<br>
        <b>Time:</b> {html.escape(str(row["timestamp"]))}<br>
        <b>Latitude:</b> {float(row["latitude"]):.6f}<br>
        <b>Longitude:</b> {float(row["longitude"]):.6f}<br>
        <b>Source:</b> {html.escape(str(row["source"]))}
    </div>
    """

    marker = folium.Marker(
        location=[
            float(row["latitude"]),
            float(row["longitude"])
        ],
        tooltip=f"{severity_value} severity - {row['road']}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(
            color=color,
            icon="exclamation-sign"
        )
    )

    if row["source"] == "Simulated test event":
        marker.add_to(live_layer)
    else:
        marker.add_to(historical_layer)

historical_layer.add_to(risk_map)
live_layer.add_to(risk_map)

folium.LayerControl(collapsed=False).add_to(risk_map)

# Save standalone HTML copy
risk_map.save(str(MAP_FILE))

# Display an interactive Folium map inside Streamlit.
# streamlit-folium avoids the deprecated components.html approach.
st_folium(
    risk_map,
    height=620,
    use_container_width=True,
    returned_objects=[]
)

st.caption(
    "Map tiles: OpenStreetMap. Marker colors indicate severity. "
    "Sample dataset coordinates are not verified accident locations."
)

st.caption(f"Standalone map saved at: {MAP_FILE}")


# --------------------------------------------------
# 6. RECENT EVENTS
# --------------------------------------------------
st.header("📋 Recent Simulated Accident Events")

if not live.empty:
    recent = live.sort_values(
        "timestamp", ascending=False
    ).head(50)

    st.dataframe(
        recent,
        width="stretch",
        hide_index=True
    )

    csv_bytes = recent.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download recent test events (CSV)",
        data=csv_bytes,
        file_name="recent_test_accidents.csv",
        mime="text/csv"
    )
else:
    st.write(
        "No test events yet. Use the test trigger above "
        "to add your first marker."
    )

st.caption(
    "The dashboard refreshes when Streamlit reruns. "
    "Automatic crash detection requires a connected sensor, "
    "camera-based model, or external accident-event feed."
)
