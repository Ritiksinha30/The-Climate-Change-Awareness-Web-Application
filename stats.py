import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def stats_page():
    
    st.set_page_config(layout="wide")

    
    st.sidebar.title("📊 Climate Indicator Menu")
    selection = st.sidebar.radio("Choose a topic", [
        "🌡 Global Temperature",
        "🌿 Green House Emissions",
        "🌊 Sea Level Rise"
    ])

    
    st.sidebar.markdown("---")

    # Main title
    col1,col2=st.columns([5,1])
    with col1:
        st.title("🌍 **Climate Change Dashboard**")
        st.markdown("Explore different aspects of global climate change using real-world data, graphs, and trends.")
    with col2:
        home=st.button("Home")
        if home:
            st.session_state.page="climate"
    
    st.markdown("---")


    if selection == "🌡 Global Temperature":
        st.header("📈 Global Temperature Trends")

        df1 = pd.read_csv(r"archive\GlobalTemperatures.csv")
        df1['dt'] = pd.to_datetime(df1['dt'])
        df1['Year'] = df1['dt'].dt.year

        avg_temp = df1.groupby('Year')['LandAverageTemperature'].mean()
        st.subheader("🌡️ Land Average Temperature Over Time")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(avg_temp.index, avg_temp.values, color='tomato', linewidth=2)
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Temperature (°C)")
        ax1.set_title("Land Average Temperature (Annual)")
        ax1.grid(True)
        st.pyplot(fig1)

        max_temp = df1.groupby('Year')['LandMaxTemperature'].mean()
        min_temp = df1.groupby('Year')['LandMinTemperature'].mean()
        st.subheader("🌡️ Max & Min Land Temperatures Over Time")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(max_temp.index, max_temp.values, label='Max Temp', color='darkred')
        ax2.plot(min_temp.index, min_temp.values, label='Min Temp', color='steelblue')
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Temperature (°C)")
        ax2.set_title("Max & Min Land Temperatures (Annual)")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

        land_ocean_temp = df1.groupby('Year')['LandAndOceanAverageTemperature'].mean()
        st.subheader("🌊 Land and Ocean Combined Temperature Over Time")
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.plot(land_ocean_temp.index, land_ocean_temp.values, color='forestgreen')
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Temperature (°C)")
        ax3.set_title("Land and Ocean Average Temperature (Annual)")
        ax3.grid(True)
        st.pyplot(fig3)

    elif selection == "🌿 Green House Emissions":
        st.header("🌍 Green House Gases Emissions")
        df2 = pd.read_csv(r"archive\climate_change.csv")
        df2['Date'] = pd.to_datetime(df2['Year'].astype(str) + '-' + df2['Month'].astype(str))
        df2.set_index('Date', inplace=True)

        st.sidebar.title("📌 Climate Variables")
        selected_vars = st.sidebar.multiselect(
            "Select variables to explore",
            ['CO2', 'CH4', 'N2O', 'CFC-11', 'CFC-12', 'TSI', 'Aerosols', 'Temp'],
            default=['CO2', 'CH4', 'Temp']
        )

        if 'CO2' in selected_vars:
            st.subheader("🌿 CO₂ Concentration Over Time")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['CO2'], color='green')
            ax.set_ylabel("CO₂ (ppm)")
            ax.grid(True)
            st.pyplot(fig)

        # === 2. CH4 over time ===
        if 'CH4' in selected_vars:
            st.subheader("🌾 Methane (CH₄) Levels Over Time")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['CH4'], color='orange')
            ax.set_ylabel("CH₄ (ppb)")
            ax.grid(True)
            st.pyplot(fig)

        # === 3. N2O over time ===
        if 'N2O' in selected_vars:
            st.subheader("💨 Nitrous Oxide (N₂O) Over Time")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['N2O'], color='purple')
            ax.set_ylabel("N₂O (ppb)")
            ax.grid(True)
            st.pyplot(fig)


        if 'CFC-11' in selected_vars or 'CFC-12' in selected_vars:
            st.subheader("🧪 CFC-11 and CFC-12 Trends")
            fig, ax = plt.subplots(figsize=(10, 4))
            if 'CFC-11' in selected_vars:
                ax.plot(df2.index, df2['CFC-11'], label='CFC-11', color='blue')
            if 'CFC-12' in selected_vars:
                ax.plot(df2.index, df2['CFC-12'], label='CFC-12', color='red')
            ax.set_ylabel("Concentration (ppt)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        if 'TSI' in selected_vars:
            st.subheader("☀️ Total Solar Irradiance (TSI)")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['TSI'], color='gold')
            ax.set_ylabel("Watts/m²")
            ax.grid(True)
            st.pyplot(fig)

        if 'Aerosols' in selected_vars:
            st.subheader("🌫️ Aerosol Optical Depth Over Time")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['Aerosols'], color='gray')
            ax.set_ylabel("Aerosol Index")
            ax.grid(True)
            st.pyplot(fig)


        if 'Temp' in selected_vars:
            st.subheader("🌡️ Global Temperature Anomaly")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df2.index, df2['Temp'], color='crimson')
            ax.set_ylabel("Temperature Anomaly (°C)")
            ax.axhline(0, color='black', linestyle='--', linewidth=1)
            ax.grid(True)
            st.pyplot(fig)

 
        st.subheader("🔗 Correlation Between All Climate Variables")
        fig, ax = plt.subplots(figsize=(10, 6))
        corr = df2[['CO2', 'CH4', 'N2O', 'CFC-11', 'CFC-12', 'TSI', 'Aerosols', 'Temp']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)


    elif selection == "🌊 Sea Level Rise":
        st.header("🌊 Sea Level Rise")
        df3 = pd.read_csv(r"archive\Global_sea_level_rise.csv")
        st.markdown("Explore the trends of global sea level rise from 1993 onward.")

        df3 = pd.read_csv(r"archive\Global_sea_level_rise.csv")
        df3['date'] = pd.to_datetime(df3['date'])
        df3['year'] = df3['year'].astype(str)

        st.sidebar.title("🌊 Sea Level Indicators")
        st.sidebar.markdown("Use the options below to customize your analysis.")

    
        st.subheader("🌊 Sea Level Rise Over Time")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(df3['date'], df3['mmfrom1993-2008average'], color='royalblue', linewidth=2)
        ax1.set_title("Sea Level Rise (1993-2020)")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Sea Level Change (mm)")
        ax1.grid(True)
        st.pyplot(fig1)


        st.subheader("📊 Sea Level Anomaly (Compared to 1993-2008 Average)")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(df3['date'], df3['mmfrom1993-2008average'] - df3['mmfrom1993-2008average'].mean(), color='seagreen')
        ax2.set_title("Sea Level Change Compared to 1993-2008 Average")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Sea Level Anomaly (mm)")
        ax2.grid(True)
        st.pyplot(fig2)

 
        st.subheader("📉 Annual Sea Level Rise Trend")
        df3['yearly_avg'] = df3.groupby('year')['mmfrom1993-2008average'].transform('mean')
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(df3['year'], df3['yearly_avg'], color='darkorange', marker='o', linestyle='--')
        ax3.set_title("Average Sea Level Rise by Year")
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Sea Level Change (mm)")
        ax3.grid(True)
        st.pyplot(fig3)


        st.subheader("📅 Monthly Sea Level Changes Over Years")
        monthly_avg = df3.groupby(df3['date'].dt.month)['mmfrom1993-2008average'].mean()
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(monthly_avg.index, monthly_avg.values, marker='x', color='purple', linestyle='-')
        ax4.set_title("Monthly Sea Level Change (Average Over Years)")
        ax4.set_xlabel("Month")
        ax4.set_ylabel("Average Sea Level Change (mm)")
        ax4.grid(True)
        st.pyplot(fig4)


        st.subheader("📊 Correlation Between Sea Level Rise and Climate Indicators")
        
        if 'Temp' in locals():  
            st.markdown("This feature would require more data integration for analysis.")
        else:
            st.markdown("⚠️ No correlation data available for this dataset yet.")


    st.markdown("---")
