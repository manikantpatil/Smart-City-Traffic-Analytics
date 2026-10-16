
from pathlib import Path
import numpy as np
import pandas as pd

# Create the data folder
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

rng = np.random.default_rng(42)

# Generate traffic records for 30 days, every 10 minutes
timestamps = pd.date_range(
    start="2026-09-01",
    periods=30 * 24 * 6,
    freq="10min"
)

roads = ["MG Road", "Station Road", "Market Road", "Ring Road"]

traffic_records = []

for timestamp in timestamps:
    for road in roads:
        hour = timestamp.hour

        # More traffic during morning and evening peak hours
        peak = 70 if hour in [8, 9, 10, 17, 18, 19] else 35

        volume = max(0, int(rng.normal(peak, 15)))
        speed = max(5, min(80, int(rng.normal(45, 12))))

        if volume > 65 and speed < 30:
            congestion = "High"
        elif volume > 40 and speed < 45:
            congestion = "Medium"
        else:
            congestion = "Low"

        traffic_records.append({
            "timestamp": timestamp,
            "road": road,
            "traffic_volume": volume,
            "avg_speed_kmph": speed,
            "congestion_level": congestion
        })

traffic = pd.DataFrame(traffic_records)
traffic.to_csv(DATA_DIR / "traffic_data.csv", index=False)

# Generate 300 simulated accident records
accident_records = []

for _ in range(300):
    road = rng.choice(roads)
    timestamp = rng.choice(timestamps)

    if road == "MG Road":
        latitude, longitude = 15.145, 74.835
    elif road == "Station Road":
        latitude, longitude = 15.150, 74.840
    elif road == "Market Road":
        latitude, longitude = 15.155, 74.830
    else:
        latitude, longitude = 15.140, 74.845

    accident_records.append({
        "timestamp": timestamp,
        "road": road,
        "latitude": latitude + rng.normal(0, 0.003),
        "longitude": longitude + rng.normal(0, 0.003),
        "severity": rng.choice(
            ["Low", "Medium", "High"],
            p=[0.50, 0.35, 0.15]
        )
    })

accidents = pd.DataFrame(accident_records)
accidents.to_csv(DATA_DIR / "accidents.csv", index=False)

print("SUCCESS! Datasets created.")
print("Traffic records:", len(traffic))
print("Accident records:", len(accidents))
print("Saved in:", DATA_DIR)
