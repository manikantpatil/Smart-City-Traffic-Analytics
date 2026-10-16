from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# Load datasets
traffic = pd.read_csv(DATA_DIR / "traffic_data.csv")
accidents = pd.read_csv(DATA_DIR / "accidents.csv")

traffic["timestamp"] = pd.to_datetime(traffic["timestamp"])
accidents["timestamp"] = pd.to_datetime(accidents["timestamp"])

print("\n===== SMART CITY TRAFFIC ANALYTICS =====")
print("Traffic records:", len(traffic))
print("Accident records:", len(accidents))

# 1. Peak-hour analysis
traffic["hour"] = traffic["timestamp"].dt.hour

hourly = traffic.groupby("hour")["traffic_volume"].mean()

print("\n===== AVERAGE TRAFFIC BY HOUR =====")
print(hourly.round(2))

plt.figure(figsize=(10, 5))
hourly.plot(kind="bar")
plt.title("Average Traffic Volume by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Traffic Volume")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "peak_hours.png")
plt.close()

# 2. Congestion analysis
congestion = traffic["congestion_level"].value_counts()

print("\n===== CONGESTION LEVELS =====")
print(congestion)

plt.figure(figsize=(7, 5))
congestion.plot(kind="bar")
plt.title("Traffic Congestion Levels")
plt.xlabel("Congestion Level")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "congestion.png")
plt.close()

# 3. Accident hotspots by road
hotspots = accidents["road"].value_counts()

print("\n===== ACCIDENTS BY ROAD =====")
print(hotspots)

plt.figure(figsize=(8, 5))
hotspots.plot(kind="bar")
plt.title("Accidents by Road")
plt.xlabel("Road")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "accident_hotspots.png")
plt.close()

# 4. Save summary reports
hourly.rename("average_traffic_volume").to_csv(
    OUTPUT_DIR / "hourly_traffic_summary.csv"
)

hotspots.rename("accident_count").to_csv(
    OUTPUT_DIR / "accident_road_summary.csv"
)

print("\nSUCCESS! Analysis completed.")
print("Charts and reports saved in:", OUTPUT_DIR)
