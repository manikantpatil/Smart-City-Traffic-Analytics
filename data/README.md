# Smart City Traffic Analytics

A Python-based data analytics project for analyzing traffic patterns, visualizing accident locations, and monitoring accident risks on interactive maps.

## Features
- Traffic data generation and analysis
- Accident data visualization
- Interactive accident maps
- Simulated live accident reporting dashboard
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
└── README.md
```

## Installation

Install Python, open the project folder in VS Code, and run:

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install pandas folium streamlit matplotlib streamlit-folium
```

## Run the Project

Generate sample data:

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

Run the main dashboard:

```bash
python -m streamlit run data/dashboard.py
```

Run the live accident reporting dashboard:

```bash
python -m streamlit run data/live_dashboard.py
```

After starting a dashboard, open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Note

Live accident reporting uses simulated input. Automatic real-world accident detection requires integration with actual sensors, cameras, or a validated detection model.

## Author

**Manikant Patil**

GitHub: https://github.com/manikantpatilgit add README.md
