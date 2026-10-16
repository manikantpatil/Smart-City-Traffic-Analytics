# Smart City Traffic Analytics

A Python-based data analytics project for analyzing traffic patterns, visualizing accident locations, and demonstrating accident-risk monitoring on a real-world map.

## Features
- Traffic data generation and analysis
- Accident data visualization
- Interactive map with accident markers
- Live accident simulation dashboard
- Accident severity monitoring
- CSV-based data storage

## Technologies Used
- Python
- Pandas
- Streamlit
- Folium
- Matplotlib
- OpenStreetMap

## Project Structure

```text
SmartCityTrafficAnalytics/
├── data/
│   ├── outputs/
│   ├── accident_map.py
│   ├── accidents.csv
│   ├── analysis.py
│   ├── dashboard.py
│   ├── live_accidents.csv
│   ├── live_dashboard.py
│   └── traffic_data.csv
├── generate_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Install Python.
2. Open the project folder in VS Code.
3. Open the terminal and run:

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Project

Generate sample traffic and accident data:

```bash
python generate_data.py
```

Run traffic analysis:

```bash
python data/analysis.py
```

Run the accident map:

```bash
python data/accident_map.py
```

Run the standard dashboard:

```bash
python -m streamlit run data/dashboard.py
```

Run the live accident simulation dashboard:

```bash
python -m streamlit run data/live_dashboard.py
```

## Note

The live accident dashboard demonstrates accident reporting using simulated input. It does not independently detect real-world accidents unless connected to an actual sensor, camera, or validated detection system.

## Author

Add your name and GitHub profile here.