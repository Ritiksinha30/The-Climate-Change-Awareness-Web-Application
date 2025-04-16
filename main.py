import streamlit as st
from loginpage import login_page, otp_verification_page  # 👈 fixed import
from signup import signup_page
from climate_change import climate_change_page
from stats import stats_page
from gallery import gallery_page
from maps import maps_page

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "otp_verify":
    otp_verification_page()
elif st.session_state.page == "climate":
    climate_change_page()
elif st.session_state.page == "stats":
    stats_page()
elif st.session_state.page == "gallery":
    gallery_page()
elif st.session_state.page == "maps":
    maps_page()
