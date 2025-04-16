import streamlit as st
from streamlit_autorefresh import st_autorefresh
import base64
import requests
import plotly.graph_objects as go
import pandas as pd


def climate_change_page():
    def go_to_login():
        st.session_state.page = "login"

    st.markdown(f"""
        <style>
            .main {{
                padding: 0rem !important;
            }}
            .block-container {{
                padding: 0rem !important;
                margin: 0 auto;
                max-width: 100%;
            }}
            body, .stApp {{
                background-color: black;
                color: white;
            }}
            .hero-container {{
                position: relative;
                text-align: left;
                color: white;
            }}
            .hero-image {{
                width: 100%;
                border-radius: 10px;
                opacity: 0.8;
            }}
            .hero-text {{
                position: absolute;
                top: 10%;
                left: 8%;
                transform: translate(0, 0);
                font-family: 'Montserrat', sans-serif;
            }}
            .hero-title {{
                font-size: 5.2vw;
                font-weight: bold;
                margin-bottom: 20px;
                line-height: 1.1;
            }}
            .hero-subtext {{
                font-size: 1.5vw;
                line-height: 1.5;
                max-width: 70%;
            }}
            .floating-fact {{
                position: absolute;
                top: 18%;
                right: 4%;
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                max-width: 300px;
                font-size: 1rem;
                font-family: 'Arial', sans-serif;
                animation: float 6s ease-in-out infinite;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10;
            }}
            @keyframes float {{
                0% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
                100% {{ transform: translateY(0); }}
            }}
            
        </style>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    
    bg_path = r"pictures\earthbgs.jpg"
    bg_base64 = get_base64_image(bg_path)

    with st.container():
        st.write("")
        st.write("")
        col1, col2,colbg, col3 = st.columns([1,2,4,3])
        with col1:
            st.markdown("<h2 style='text-align: center;'>Search</h2>", unsafe_allow_html=True)
        with col2:
            search = st.text_input("") 
              
        with colbg:
            st.write("")
        with col3:
            with st.container():
                col4, col5 = st.columns([4, 1])
                with col5:
                    st.write("")
                    if st.button("LOGIN"):
                        go_to_login()
                    
            with st.container():
                nav1, nav2, nav3, nav4 = st.columns(4)
                with nav1:
                    if st.button("📊 Stats"):
                        st.session_state.page = "stats"
                with nav2:
                    if st.button("🗺️ Maps"):
                        st.session_state.page = "maps"
                with nav3:
                    if st.button("🖼️ Gallery"):
                        st.session_state.page = "gallery"
                with nav4:
                    if st.button("ℹ️ About"):
                        st.session_state.page = "about"

    st_autorefresh(interval=10 * 1000, limit=None, key="auto_refresh")
    facts = [
        "🌍 The last 8 years have been the warmest on record globally. [WMO, 2023]",
        "🌡️ 2023 was the hottest year ever recorded. [NASA, 2023]",
        "🌊 Sea levels have risen over 8 inches since 1880. [NOAA]",
        "🧊 Arctic sea ice is declining at a rate of 13% per decade. [NASA]",
        "🔥 Wildfires are becoming more frequent and intense due to climate change.",
        "🌪️ Extreme weather events have increased fivefold over the past 50 years. [WMO]",
        "🌱 Climate change threatens food security and crop yields worldwide.",
        "🌫️ Air pollution from fossil fuels kills 8.7 million people annually. [Harvard Study]",
        "💧 Over 1.2 billion people are at risk due to water scarcity linked to climate change.",
        "🦋 One million species are at risk of extinction due to climate disruption. [IPBES]",
    ]

    if "fact_index" not in st.session_state:
        st.session_state.fact_index = 0
    else:
        st.session_state.fact_index = (st.session_state.fact_index + 1) % len(facts)
        
    st.markdown(f"""
        <div class="hero-container">
            <img src="{bg_base64}" class="hero-image"/>
            <div class="hero-text">
                <div class="hero-title">Climate<br>Change</div>
                <div class="hero-subtext">
                    Rising temperatures, melting ice caps,
                    <br>and extreme weather are no longer predictions —
                    <br>they're reality. Climate change is here.
                    Let's respond with urgency and purpose.
                </div>
            </div>
        </div>
        <div class="floating-fact">
            {facts[st.session_state.fact_index]}
        </div>
    """, unsafe_allow_html=True)


    st.markdown("---")

    st.markdown("## 🌍 Real-time Climate Indicators")
   
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="🌡 Global Avg Temp (March '24)", value="1.58°C ↑", delta="+0.2°C vs March '23")
        st.caption("Source: NOAA/NASA")

    with col2:
        def get_co2_concentration():
            response = requests.get("https://global-warming.org/api/co2-api")
            if response.status_code == 200:
                data = response.json()
                co2_data = data['co2']
                if len(co2_data) >= 2:
                    latest = float(co2_data[-1]['trend'])
                    previous = float(co2_data[-2]['trend'])
                    delta = latest - previous
                    return latest, delta
            st.error("Failed to fetch CO₂ data.")
            return None, None

        co2, delta = get_co2_concentration()

        if co2 is not None:
            delta_str = f"{delta:+.2f} ppm"  
            st.metric(
                label="🟢 CO₂ Concentration",
                value=f"{co2:.2f} ppm",
                delta=delta_str
            )
            st.caption("Source: global-warming.org")
    with col3:
        def get_sea_level_rise():
            station_id = '8454000'  
            url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?" \
                f"product=water_level&application=web_services&begin_date=20250101&" \
                f"end_date=20250114&datum=MLLW&station={station_id}&time_zone=GMT&" \
                f"units=metric&format=json"
            
            try:
                response = requests.get(url)
                response.raise_for_status()  
                
                data = response.json()
                if 'data' in data and data['data']:
                    latest = float(data['data'][-1]['v'])
                    previous = float(data['data'][-2]['v']) if len(data['data']) > 1 else latest
                    delta = latest - previous
                    return latest, delta
                else:
                    print("No water level data available.")
                    return None, None
            except requests.exceptions.RequestException as e:
                print(f"Error fetching sea level data: {e}")
                return None, None

        sea_level, delta_sea = get_sea_level_rise()

        if sea_level is not None:
            delta_str = f"{delta_sea:+.2f} mm"
            st.metric(
                label="🌊 Sea Level Rise",
                value=f"{sea_level:.2f} mm",
                delta=delta_str
            )
            st.caption("Source: NOAA CO-OPS")
    st.markdown(
        """
        📊 These indicators show how climate is rapidly changing — 
        affecting ecosystems, weather patterns, and human life globally.
        """
    )
    st.markdown("---")

    st.markdown("## 📈 Historical Trends")

    def load_co2_history():
        response = requests.get("https://global-warming.org/api/co2-api")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['co2'])
            df['year'] = pd.to_datetime(df['year'], errors='coerce')
            df['trend'] = pd.to_numeric(df['trend'], errors='coerce')
            return df.dropna(subset=['year', 'trend'])
        return pd.DataFrame()

    co2_df = load_co2_history()
    if not co2_df.empty:
        fig_co2 = go.Figure()
        fig_co2.add_trace(go.Scatter(x=co2_df['year'], y=co2_df['trend'], mode='lines', name='CO₂ (ppm)', line=dict(color='green')))
        fig_co2.update_layout(title="CO₂ Concentration Over Time", xaxis_title="Year", yaxis_title="CO₂ (ppm)", template='plotly_dark')
        st.plotly_chart(fig_co2, use_container_width=True)


    def load_temperature_history():
        latitude = 28.6139
        longitude = 77.2090
        start_date = "2000-01-01"
        end_date = "2020-12-31"
        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}"
            f"&daily=temperature_2m_max&timezone=Asia%2FKolkata"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            dates = data['daily']['time']
            temps = data['daily']['temperature_2m_max']
            df = pd.DataFrame({'date': pd.to_datetime(dates), 'max_temp': temps})
            df['year'] = df['date'].dt.year
            df_grouped = df.groupby('year')['max_temp'].mean().reset_index()
            return df_grouped
        return pd.DataFrame()


    temp_df = load_temperature_history()
    if not temp_df.empty:
        fig_temp = go.Figure()
        fig_temp.add_trace(
            go.Scatter(
                x=temp_df['year'],
                y=temp_df['max_temp'],
                mode='lines',
                name='Max Temp (°C)',
                line=dict(color='orange')
            )
        )
        fig_temp.update_layout(
            title="Annual Max Temperature Over Time",
            xaxis_title="Year",
            yaxis_title="Max Temperature (°C)",
            template='plotly_dark'
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        

    def load_sea_level_history():
        station_id = '8454000'  
        begin_date = '20000101'
        end_date = '20201231'
        url = (
            f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
            f"product=monthly_mean&application=climate_app&begin_date={begin_date}&end_date={end_date}"
            f"&datum=MLLW&station={station_id}&time_zone=GMT&units=metric&format=json"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                df = pd.DataFrame(data['data'])
             
                df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
             
                df['MSL'] = pd.to_numeric(df['MSL'], errors='coerce')
             
                df = df.dropna(subset=['MSL'])
               
                df['year'] = df['date'].dt.year
                
                df_grouped = df.groupby('year')['MSL'].mean().reset_index()
                return df_grouped
        return pd.DataFrame()

    sea_df = load_sea_level_history()
    if not sea_df.empty:
        fig_sea = go.Figure()
        fig_sea.add_trace(
            go.Scatter(
                x=sea_df['year'],
                y=sea_df['MSL'],
                mode='lines',
                name='Sea Level (mm)',
                line=dict(color='blue')
            )
        )
        fig_sea.update_layout(
            title="Annual Mean Sea Level Over Time",
            xaxis_title="Year",
            yaxis_title="Sea Level (mm)",
            template='plotly_dark'
        )
        st.plotly_chart(fig_sea, use_container_width=True)
