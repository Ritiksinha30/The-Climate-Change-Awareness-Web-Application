import streamlit as st

def otp_verification_page():
    st.title("OTP Verification")
    st.markdown("Enter the 6-digit OTP sent to your email.")

    user_otp = st.text_input("OTP", max_chars=6)

    if st.button("Verify OTP"):
        if user_otp == st.session_state.get("temp_otp"):
            st.success(" OTP verified! You’re logged in.")
            st.session_state.page = "climate"
        else:
            st.error(" Incorrect OTP. Please try again.")
