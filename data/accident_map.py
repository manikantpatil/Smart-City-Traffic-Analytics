
from pathlib import Path

import pandas as pd
import folium
from folium.plugins import HeatMap, Fullscreen

# Project paths
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "accidents.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAP_FILE = OUTPUT_DIR / "accident_risk_map.html"

# Load accident records
if not CSV_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

accidents = pd.read_csv(CSV_FILE)

required = ["latitude", "longitude", "severity"]
missing = [col for col in required if col not in accidents.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Clean GPS coordinates
for col in ["latitude", "longitude"]:
    accidents[col] = pd.to_numeric(
        accidents[col], errors="coerce"
    )

accidents = accidents.dropna(
    subset=["latitude", "longitude"]
).copy()

# Remove invalid GPS coordinates
accidents = accidents[
    accidents["latitude"].between(-90, 90)
    & accidents["longitude"].between(-180, 180)
].copy()

if accidents.empty:
    raise ValueError("No valid GPS coordinates found.")

# Create real-world street map
center = [
    accidents["latitude"].mean(),
    accidents["longitude"].mean()
]

risk_map = folium.Map(
    location=center,
    zoom_start=13,
    tiles="OpenStreetMap",
    control_scale=True
)

Fullscreen().add_to(risk_map)

# Accident concentration heatmap
heat_layer = folium.FeatureGroup(
    name="Accident Heatmap",
    show=True
)

heat_data = accidents[
    ["latitude", "longitude"]
].values.tolist()

HeatMap(
    heat_data,
    radius=20,
    blur=15,
    min_opacity=0.35
).add_to(heat_layer)

heat_layer.add_to(risk_map)

# Individual accident markers
marker_layer = folium.FeatureGroup(
    name="Accident Locations",
    show=True
)

for index, row in accidents.iterrows():
    severity = str(row["severity"]).strip().title()

    if severity == "High":
        color = "red"
    elif severity == "Medium":
        color = "orange"
    else:
        color = "green"

    road = row.get("road", "Unknown")
    timestamp = row.get("timestamp", "Not available")

    popup_html = f"""
    <div style="width:220px">
        <h4>🚨 Accident Record #{index + 1}</h4>
        <b>Road:</b> {road}<br>
        <b>Severity:</b> {severity}<br>
        <b>Time:</b> {timestamp}<br>
        <b>Latitude:</b> {row['latitude']:.6f}<br>
        <b>Longitude:</b> {row['longitude']:.6f}
    </div>
    """

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        tooltip=f"Accident: {severity}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(
            color=color,
            icon="exclamation-sign"
        )
    ).add_to(marker_layer)

marker_layer.add_to(risk_map)

# Zoom to the accident locations
if len(accidents) > 1:
    risk_map.fit_bounds(
        [
            [accidents["latitude"].min(),
             accidents["longitude"].min()],
            [accidents["latitude"].max(),
             accidents["longitude"].max()]
        ],
        padding=(25, 25)
    )

# Show and hide map layers
folium.LayerControl(collapsed=False).add_to(risk_map)

# Map legend
legend = """
<div style="
position: fixed; bottom: 25px; left: 25px; z-index: 9999;
background: white; color: black; padding: 12px;
border: 1px solid grey; border-radius: 6px;">
<b>Accident Severity</b><br>
<span style="color:red">●</span> High<br>
<span style="color:orange">●</span> Medium<br>
<span style="color:green">●</span> Low
</div>
"""

risk_map.get_root().html.add_child(
    folium.Element(legend)
)

# Save map
risk_map.save(str(MAP_FILE))

print("SUCCESS: Real-world accident map created.")
print(f"Accident records displayed: {len(accidents)}")
print(f"Map saved to: {MAP_FILE}")
