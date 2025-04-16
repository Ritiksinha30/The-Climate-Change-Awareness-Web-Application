import streamlit as st
import geopandas as gpd
import numpy as np
import folium
from streamlit_folium import st_folium

def maps_page():
    with st.container():
        col1,col2=st.columns([6,1])
        with col1:
            st.title("🌍 Climate Impact Dashboard")
        with col2:
            home=st.button("Home")
            if home:
                st.session_state.page="climate"

    option = st.sidebar.selectbox(
        "Choose a simulation to view:",
        ("Rising Sea Levels", "Heat Waves", "Air Quality Index", "Global Temperature")
    )


    gdf = gpd.read_file("world-administrative-boundaries.shp")
    gdf = gdf.to_crs(epsg=4326)


    np.random.seed(42)
    gdf["Sea_Level_Risk"] = np.random.uniform(0, 100, len(gdf))
    gdf["Heatwave_Index"] = np.random.uniform(20, 50, len(gdf))
    gdf["AQI"] = np.random.randint(50, 200, len(gdf))
    gdf["Avg_Temperature"] = np.random.uniform(10, 35, len(gdf))


    m = folium.Map(location=[20, 0], zoom_start=2)

    if option == "Rising Sea Levels":
        st.header("🌊 Rising Sea Level Risk")
        data_column = "Sea_Level_Risk"
        legend = "Risk Level (%)"
        color = "Blues"

    elif option == "Heat Waves":
        st.header("🔥 Heatwave Intensity Index")
        data_column = "Heatwave_Index"
        legend = "Heatwave Index"
        color = "OrRd"

    elif option == "Air Quality Index":
        st.header("🌫 Air Quality Index (AQI)")
        data_column = "AQI"
        legend = "AQI"
        color = "YlGnBu"

    elif option == "Global Temperature":
        st.header("🌡 Global Average Temperature")
        data_column = "Avg_Temperature"
        legend = "Temperature (°C)"
        color = "YlOrRd"

    folium.Choropleth(
        geo_data=gdf,
        name="choropleth",
        data=gdf,
        columns=[gdf.index, data_column],
        key_on="feature.id",
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend,
    ).add_to(m)

    # Show the map
    st_folium(m, width=700,height=500)