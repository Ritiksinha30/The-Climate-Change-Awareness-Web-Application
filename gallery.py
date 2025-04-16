import streamlit as st
from PIL import Image

def gallery_page():
    st.set_page_config(page_title="🌍 Climate Change Gallery", layout="wide")
    with st.container():
        st.write("")
        st.write("")
        col1,col2=st.columns([1,7])
        with col1:
            home=st.button("Home")
            if home:
                st.session_state.page="climate"
        with col2:
            st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🌱 Climate Change Awareness Gallery</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size:18px;'>Explore the environmental challenges impacting our planet and the efforts to combat them.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Image data
    gallery = [
        {
            "file": "pictures/Melting Glacier.jpg",
            "title": "Melting Glaciers",
            "desc": "Glaciers around the world are retreating due to rising temperatures.",
            "fact": "Between 2000 and 2019, the world's glaciers lost an average of 267 billion tons of ice each year.",
            "solution": "Drastically reducing carbon emissions and transitioning to renewable energy is essential to slowing glacier melt."
        },
        {
            "file": "pictures/wildfire.jpg",
            "title": "Wildfires",
            "desc": "Rising global temperatures increase wildfire frequency and severity.",
            "fact": "In 2020, wildfires in California alone released more CO₂ than the entire state's power sector.",
            "solution": "Forest management, climate action, and early detection systems can reduce wildfire impact."
        },
        {
            "file": "pictures/Flood.jpg",
            "title": "Flooding Events",
            "desc": "Sea-level rise and heavy rains increase flooding risks worldwide.",
            "fact": "Climate change could displace over 1 billion people due to flooding by 2050.",
            "solution": "Improved urban planning, levees, and green infrastructure help manage floods."
        },
        {
            "file": "pictures/Deforestation.jpg",
            "title": "Deforestation",
            "desc": "The removal of forests contributes to global warming and habitat loss.",
            "fact": "Forests absorb 2.6 billion tons of carbon dioxide per year – deforestation reverses this benefit.",
            "solution": "Support reforestation efforts, responsible agriculture, and enforce anti-logging laws."
        },
        {
            "file": "pictures/Polar Bear.jpg",
            "title": "Arctic Habitat Loss",
            "desc": "Melting ice threatens Arctic wildlife like polar bears and seals.",
            "fact": "The Arctic is warming 4 times faster than the global average.",
            "solution": "Protecting Arctic zones and global climate pledges are key to preserving biodiversity."
        },
        {
            "file": "pictures/Pollution.jpg",
            "title": "Industrial Pollution",
            "desc": "Fossil fuel industries are top contributors to greenhouse gas emissions.",
            "fact": "The top 100 fossil fuel producers are linked to over 70% of global emissions since 1988.",
            "solution": "Stronger regulations, clean energy investment, and carbon taxes are impactful steps."
        },
        {
            "file": "pictures/Drought.jpg",
            "title": "Severe Droughts",
            "desc": "Extended dry periods devastate crops and limit access to clean water.",
            "fact": "Over 2.3 billion people currently live in water-stressed countries.",
            "solution": "Water conservation tech and climate-adapted agriculture can increase resilience."
        },
        {
            "file": "pictures/Renewable Energy.jpg",
            "title": "Clean Energy Future",
            "desc": "Solar, wind, and hydropower are crucial to fighting climate change.",
            "fact": "Renewables generated 30% of the world’s electricity in 2023.",
            "solution": "Global cooperation and subsidies can accelerate the green energy transition."
        }
    ]

    cols = st.columns(4)

    for i, item in enumerate(gallery):
        with cols[i % 4]:
            st.image(item["file"], use_container_width=True)
            st.markdown(f"<h4 style='color: #1abc9c; margin-bottom: 0.3rem;'>{item['title']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 14px; color: #7f8c8d;'>{item['desc']}</p>", unsafe_allow_html=True)
            
            with st.expander("📊 More Info"):
                st.markdown(f"<b>🌡️ Fact:</b> {item['fact']}", unsafe_allow_html=True)
                st.markdown(f"<b>✅ Solution:</b> {item['solution']}", unsafe_allow_html=True)

    # Styling
    st.markdown("""
        <style>
            .stImage > img {
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
                transition: 0.3s ease-in-out;
            }
            .stImage:hover > img {
                transform: scale(1.02);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            }
            .block-container {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")