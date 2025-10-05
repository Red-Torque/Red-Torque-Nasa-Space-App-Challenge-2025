import streamlit as st
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import glob
from streamlit_folium import st_folium
import folium

# ------------------- Settings -------------------
trmm_folder = r"C:/Users/alan/Downloads/TRMM_3B42_Daily_7"
gldas_folder = r"C:/Users/alan/Downloads/GLDAS_NOAH025_M_2.1-20251004_193114"
precip_var = "HQprecipitation"
temp_var = "Tair_f_inst"
rain_threshold = 2.5
sat_layer = "MODIS_Terra_CorrectedReflectance_TrueColor"

geolocator = Nominatim(user_agent="weather_app")

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="🌌 Will it rain on my Parade", layout="wide")

# Light / modern theme
st.markdown("""
    <style>
        body {background-color: #F9FAFB; color: #111827;}
        .stTextInput>div>div>input {background-color: #FFFFFF; color: #111827;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align:center; color:white; background-color:#0b3d91; padding:15px; border-radius:10px;'>
    🌦 Will It Rain on My Parade? 🌦
    </h1>
""", unsafe_allow_html=True)

st.markdown("### Enter a city or pick a location on the map to analyze weather trends:")

# ------------------- City Input -------------------
col1, col2 = st.columns([3, 1])

with col1:
    city = st.text_input("City/Place:", placeholder="Enter city name")



with col2:
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    if st.button("Get Coordinates"):
        if city:
            try:
                location = geolocator.geocode(f"{city}, India")
                if location:
                    lat = float(location.latitude)
                    lon = float(location.longitude)
                    st.session_state['lat'] = lat
                    st.session_state['lon'] = lon
                    st.success(f"Coordinates: Latitude {lat:.4f}, Longitude {lon:.4f}")
                else:
                    st.error("City not found! Try entering manually.")
            except Exception as e:
                st.error(f"Error: {e}")

# ------------------- Interactive Map -------------------
st.markdown("### 🗺 Select a Location on the Map (India)")
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB positron")

if "lat" in st.session_state and "lon" in st.session_state:
    folium.Marker(
        [st.session_state["lat"], st.session_state["lon"]],
        tooltip="Selected Location",
        icon=folium.Icon(color="blue")
    ).add_to(m)

map_data = st_folium(m, height=400, width=700)

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.session_state['lat'] = lat
    st.session_state['lon'] = lon
    st.success(f"📍 Selected on Map: Latitude {lat:.4f}, Longitude {lon:.4f}")

lat = st.session_state.get('lat', 20.5937)
lon = st.session_state.get('lon', 78.9629)
st.markdown(f"Selected Coordinates: Latitude: {lat:.4f}, Longitude: {lon:.4f}")

target_date = st.date_input("Select Date", datetime.today())

# ------------------- Weather Analysis -------------------
if st.button("Run Weather Analysis"):
    with st.spinner('Please wait, loading NASA data and analyzing... 🌍'):
        # ------------------- Load TRMM -------------------
        trmm_files = sorted(glob.glob(trmm_folder + "/*.nc4"))
        precip_records = []
        for file in trmm_files:
            try:
                ds = xr.open_dataset(file)
                precip_sel = ds[precip_var].sel(lat=lat, lon=lon, method="nearest")
                if 'time' in precip_sel.dims:
                    precip_val = float(precip_sel.isel(time=0).values)
                    date_val = pd.to_datetime(precip_sel['time'].isel(time=0).values)
                else:
                    precip_val = float(precip_sel.values)
                    date_val = pd.to_datetime(file.split('.')[-3])
                precip_records.append({'date': date_val, 'precip_mm': precip_val})
                ds.close()
            except:
                continue
        df_precip = pd.DataFrame(precip_records)

        # ------------------- Load GLDAS -------------------
        gldas_files = sorted(glob.glob(gldas_folder + "/*.nc4"))
        temp_records = []
        for file in gldas_files:
            try:
                ds = xr.open_dataset(file)
                temp_sel = ds[temp_var].sel(lat=lat, lon=lon, method="nearest")
                if 'time' in temp_sel.dims:
                    temp_val = float(temp_sel.isel(time=0).values) - 273.15
                    date_val = pd.to_datetime(temp_sel['time'].isel(time=0).values)
                else:
                    temp_val = float(temp_sel.values) - 273.15
                    fname = file.split('/')[-1]
                    year = int(fname.split('.')[1][1:5])
                    month = int(fname.split('.')[1][5:7])
                    date_val = pd.to_datetime(f"{year}-{month:02d}-15")
                temp_records.append({'date': date_val, 'temperature_C': temp_val})
                ds.close()
            except:
                continue
        df_temp = pd.DataFrame(temp_records)

        # ------------------- Compute Rain Probability -------------------
        target_month = target_date.month
        target_day = target_date.day
        df_precip['day_of_year'] = df_precip['date'].dt.dayofyear
        target_doy = pd.Timestamp(year=2000, month=target_month, day=target_day).dayofyear
        doy_range = list(range(target_doy-5, target_doy+6))
        subset_precip = df_precip[df_precip['day_of_year'].isin(doy_range)]
        num_rainy_days = (subset_precip['precip_mm'] >= rain_threshold).sum()
        total_days = len(subset_precip)
        rain_prob = num_rainy_days / total_days if total_days > 0 else 0
        avg_precip = subset_precip['precip_mm'].mean()
        avg_temp = df_temp[df_temp['date'].dt.month == target_month]['temperature_C'].mean()

        # ------------------- Display Results -------------------
        st.markdown(f"""
        <div style='background-color:#E3F2FD; padding:15px; border-radius:10px;'>
            <h2 style='color:#0D47A1;'>🌦 Weather Analysis Results 🌦</h2>
            <p style='font-size:20px;'>☔ Average precipitation: <b>{avg_precip:.2f} mm/day</b></p>
            <p style='font-size:20px;'>💧 Rain probability: <b>{rain_prob*100:.2f}%</b></p>
            <p style='font-size:20px;'>🌡 Average temperature: <b>{avg_temp:.2f} °C</b></p>
        </div>
        """, unsafe_allow_html=True)

        if rain_prob > 0.5:
            st.markdown("<h3 style='color:#ef5350;'>☔ Better grab an umbrella!</h3>", unsafe_allow_html=True)
        elif rain_prob > 0.2:
            st.markdown("<h3 style='color:#fbc02d;'>🌂 Might need a raincoat just in case!</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:#388e3c;'>☀ Probably safe, enjoy the sun!</h3>", unsafe_allow_html=True)

        # ------------------- Plots -------------------
        st.markdown("### 📊 Historical Data")
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        for year, group in df_precip.groupby(df_precip['date'].dt.year):
            ax[0].plot(group['date'].dt.dayofyear, group['precip_mm'], label=str(year))
        ax[0].set_title("Daily Precipitation by Year")
        ax[0].set_ylabel("Precipitation (mm)")
        ax[0].grid(True)
        ax[0].legend()

        for year, group in df_temp.groupby(df_temp['date'].dt.year):
            ax[1].plot(group['date'].dt.month, group['temperature_C'], label=str(year))
        ax[1].set_title("Monthly Temperature by Year")
        ax[1].set_xlabel("Month")
        ax[1].set_ylabel("Temperature (°C)")
        ax[1].grid(True)
        ax[1].legend()

        st.pyplot(fig)

        # ------------------- Satellite Images -------------------
        st.markdown("### 🛰 Satellite Images (Last 5 Years)")
        bbox = [lat - 0.25, lon - 0.25, lat + 0.25, lon + 0.25]
        today = datetime.today()
        cols = st.columns(5)
        for i in range(5):
            year = today.year - i
            date_str = f"{year}-{target_date.month:02d}-{target_date.day:02d}"
            url = (
                f"https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?"
                f"SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS={sat_layer}&"
                f"STYLES=&CRS=EPSG:4326&BBOX={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}&"
                f"WIDTH=512&HEIGHT=512&FORMAT=image/png&TIME={date_str}"
            )
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((200, 200))
                    cols[i].image(img, caption=str(year))
                else:
                    cols[i].write(f"No image for {year}")
            except:
                cols[i].write(f"Error loading {year}")
