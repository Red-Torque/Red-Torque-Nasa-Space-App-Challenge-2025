# Project Title

**RT WEatherSense – A NASA-powered Weather Insight & Prediction App by Team Red Torque**

## What It Does

“”RT WEatherSense is an interactive web application built using **Streamlit**. It analyzes real NASA Earth observation data to provide **rainfall probabilities, temperature trends, and satellite imagery** for any location in India.

**Key functionalities include:**

* Selecting a city or clicking on a live map to get accurate coordinates.
* Analyzing weather data from **TRMM** and **GLDAS** datasets.
* Estimating rainfall probability for a chosen date using historical precipitation records.
* Viewing historical temperature and rainfall trends.
* Accessing **MODIS satellite imagery** for the past five years around the selected region.
* A clean, user-friendly interface designed for both technical and non-technical users.

## Benefits and Impact

**Benefits:**

* Provides localized climate insights without requiring coding knowledge.
* Helps communities and event organizers anticipate rainfall using real historical data.
* Encourages awareness of climate variability and the importance of Earth observation.
* Demonstrates how open data and citizen science can support sustainable decisions in agriculture, urban planning, and disaster preparedness.

**Impact:**

* Bridges the gap between raw scientific datasets and public understanding.
* Turns large amounts of satellite data into an intuitive story of Earth’s weather systems.

## Tools, Technologies, and Datasets

**Software & Libraries:**

* Streamlit for the web application
* Folium + Streamlit-Folium for interactive maps
* Matplotlib for rainfall and temperature plots
* Xarray & Pandas for handling large NetCDF datasets
* Geopy for geocoding city names
* Pillow and Requests for displaying NASA MODIS imagery

**Datasets:**

* TRMM 3B42 Daily – precipitation
* GLDAS NOAH L4 Model – surface temperature
* MODIS Terra – satellite imagery

**Languages:** Python 3.11
**Hardware:** Standard personal computer capable of processing NASA NetCDF datasets

## Creativity and Technical Achievements

* Real-time rendering of MODIS satellite imagery using NASA WMS services.
* Combines spatial (map-based) and temporal (historical trends) analysis.
* Engaging, modern dashboard design that balances scientific accuracy with accessibility.
* Built entirely from open-source tools and NASA datasets for reproducibility.

## Alignment with NASA Space Apps 2025 Criteria

* **Impact:** Promotes understanding of NASA Earth data for local climate awareness.
* **Use of Data:** Integrates multiple NASA datasets meaningfully.
* **Creativity:** Combines accessibility, interactive design, and technical depth.
* **Technical Achievement:** Efficiently handles multi-dimensional NetCDF data and satellite imagery.
* **Presentation:** Polished, easy-to-navigate interface with clear visualization.

## Future Extensions

* AI-based rainfall prediction models using TRMM data.
* Integration of GPM IMERG and Sentinel datasets for higher resolution.
* Global coverage with region filters and animated visualizations.
* API version for mobile or third-party integration.

## Summary

“RT WEatherSense” is a Streamlit-based weather analysis app by Team Red Torque that uses NASA satellite data (**TRMM, GLDAS, MODIS**) to provide rainfall probabilities, temperature trends, and satellite imagery for locations across India. Users can select a city or click on a map to get precise coordinates, view historical rainfall and temperature trends, and explore MODIS images from the past five years. The app turns complex NASA datasets into a simple, interactive dashboard accessible to both researchers and the general public.

The app processes large NASA NetCDF datasets using Python libraries like **Pandas, Xarray, Matplotlib, and Folium**. It combines spatial interaction (map selection) with temporal analysis (historical trends) in one user-friendly interface. MODIS imagery is fetched in real-time from NASA’s WMS servers, creating a visually engaging and scientifically accurate experience.

This project makes open NASA data practical and understandable, supporting decision-making for students, researchers, event planners, and communities. Future improvements include AI-based rainfall prediction, integration of higher-resolution datasets, global coverage, and an API version. “Will It Rain on My Parade?” demonstrates how open data, coding, and creativity can transform massive climate datasets into actionable insights.
