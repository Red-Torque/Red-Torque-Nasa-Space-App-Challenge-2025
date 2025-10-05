# 🌦 RT WeatherSense

A *Streamlit* app to explore weather trends for any location in India using NASA TRMM and GLDAS datasets.  
Predicts rain probability, displays historical weather trends, and shows satellite imagery.

---

## *Features*

- *Location Selection*
  - Enter a city name to fetch coordinates automatically.
  - Select a location interactively on the map.

- *Weather Analysis*
  - Computes rain probability based on historical TRMM data.
  - Displays average precipitation and temperature.

- *Visualizations*
  - Historical daily precipitation plots.
  - Monthly temperature trends by year.

- *Satellite Imagery*
  - Displays MODIS Terra satellite images for the selected location for the past 5 years.

---

## *Datasets Required*

1. *TRMM 3B42 Daily Precipitation Data*
   - Dataset: [TRMM 3B42 Daily Version 7](https://disc.gsfc.nasa.gov/datasets/TRMM_3B42_Daily_7/summary)
   - Place downloaded .nc4 files in:  
     C:/Users/alan/Downloads/TRMM_3B42_Daily_7

2. *GLDAS NOAH Land Surface Model Data*
   - Dataset: [GLDAS Noah Land Surface Model L4 0.25° × 0.25°](https://disc.gsfc.nasa.gov/datasets/FLDAS_NOAH025_M_2.1/summary)
   - Place downloaded .nc4 files in:  
     C:/Users/alan/Downloads/GLDAS_NOAH025_M_2.1-20251004_193114

> *Tip:* You can download these datasets through NASA Earthdata Search or via OPeNDAP links.

---

## *Requirements*

Python 3.9+ and the following packages:
streamlit
pandas
numpy
xarray
matplotlib
Pillow
requests
geopy
folium
streamlit-folium
