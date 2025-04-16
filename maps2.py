import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Load the shapefile
st.set_page_config(layout="wide")
gdf = gpd.read_file("world-administrative-boundaries.shp")
gdf = gdf.to_crs(epsg=4326)

# Simulated data for sea level rise and heatwaves
np.random.seed(42)
gdf["Sea_Level_Risk"] = np.random.uniform(0, 100, len(gdf))
gdf["Heatwave_Index"] = np.random.uniform(20, 50, len(gdf))

# Fetch AQI data from OpenAQ
aqi_url = "https://data.giss.nasa.gov/gistemp/"
response = requests.get(aqi_url)
data = response.json()
results = data.get('results', [])
df_aqi = pd.json_normalize(results)

def extract_pm25(measurements):
    for m in measurements:
        if m['parameter'] == 'pm25':
            return m['value']
    return None

df_aqi['pm25'] = df_aqi['measurements'].apply(extract_pm25)

# Load global temperature anomalies data
try:
    df_temp = pd.read_csv('GLB.Ts+dSST.csv', skiprows=1)
    df_temp = df_temp[['Year', 'J-D']]
    df_temp.columns = ['Year', 'Anomaly']
    df_temp.dropna(inplace=True)
    df_temp['Anomaly'] = pd.to_numeric(df_temp['Anomaly'], errors='coerce')
except FileNotFoundError:
    df_temp = pd.DataFrame({'Year': [], 'Anomaly': []})

# Streamlit UI
st.title("🌍 Real-Time Climate Impact Dashboard")

option = st.sidebar.selectbox(
    "Select a Climate Indicator:",
    ("Rising Sea Levels", "Heat Waves", "Air Quality Index", "Global Temperature Anomalies")
)

# Visualization Logic
if option == "Rising Sea Levels":
    st.header("🌊 Rising Sea Level Risk")
    col = "Sea_Level_Risk"
    cmap = "Blues"
elif option == "Heat Waves":
    st.header("🔥 Heatwave Index")
    col = "Heatwave_Index"
    cmap = "OrRd"
elif option == "Air Quality Index":
    st.header("🌫 Real-Time PM2.5 AQI (India)")

    st.write("Top 10 Cities by PM2.5 Levels:")
    st.dataframe(df_aqi[['city', 'pm25']].sort_values('pm25', ascending=False).head(10))

    st.map(df_aqi[['coordinates.latitude', 'coordinates.longitude']].rename(
        columns={'coordinates.latitude': 'lat', 'coordinates.longitude': 'lon'}
    ))

    st.stop()
elif option == "Global Temperature Anomalies":
    st.header("🌡 Global Temperature Anomalies (NASA GISTEMP)")

    if df_temp.empty:
        st.error("Temperature anomaly dataset not found. Please ensure 'GLB.Ts+dSST.csv' is available.")
    else:
        fig, ax = plt.subplots()
        ax.plot(df_temp['Year'], df_temp['Anomaly'], color='red')
        ax.set_title("Global Temperature Anomalies Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Temperature Anomaly (°C)")
        st.pyplot(fig)

    st.stop()

# Create Folium map for geographic indicators
m = folium.Map(location=[20, 0], zoom_start=2)

folium.Choropleth(
    geo_data=gdf,
    data=gdf,
    columns=[gdf.index, col],
    key_on="feature.id",
    fill_color=cmap,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=col,
).add_to(m)

st_folium(m, width=700, height=500)
