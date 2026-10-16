# Smart City Traffic Analytics

A Python-based project for analyzing traffic patterns, identifying accident hotspots, and visualizing accident locations using interactive maps and dashboards.

## Features
- Traffic and congestion analysis
- Accident hotspot mapping
- Accident severity monitoring
- Interactive maps
- Simulated live accident reporting

## Technologies
- Python
- Pandas
- Streamlit
- Folium
- Matplotlib
- OpenStreetMap

## How to Run

Install the required libraries:

```bash
pip install pandas folium streamlit matplotlib streamlit-folium
```

Run traffic analysis:

```bash
python data/analysis.py
```

Run the dashboard:

```bash
python -m streamlit run data/dashboard.py
```

Run the live accident dashboard:

```bash
python -m streamlit run data/live_dashboard.py
```

## Note
Live accident reporting is simulated and does not independently detect real-world accidents.

## Author
Manikant Patil

## GitHub
https://github.com/manikantpatil/Smart-City-Traffic-Analytics
