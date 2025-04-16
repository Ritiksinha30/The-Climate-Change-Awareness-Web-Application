import streamlit as st
import sqlite3
import hashlib
import base64
import smtplib
import random

# Send OTP email
def send_otp_email(receiver_email, otp_code):
    sender_email = "pk821246@gmail.com"
    sender_password = st.secrets["email_password"]

    message = f"""Subject: Your OTP Code

Your login OTP is: {otp_code}
"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send OTP. Error: {e}")
        return False

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authenticate from DB
def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

# Login Page
def login_page():
    st.markdown('<style>.main{padding:0}.block-container{padding:0;margin:auto;max-width:100%}.login-box{background:rgba(0,0,0,0.7);border-radius:15px;padding:2rem;color:white}</style>', unsafe_allow_html=True)

    if st.button("Back to Home"):
        st.session_state.page = "climate"

    col1, col2 = st.columns([3, 2])
    with col1:
        bg_path = "loginbg.jpg"
        try:
            with open(bg_path, "rb") as image_file:
                encoded_bg = base64.b64encode(image_file.read()).decode()
                st.markdown(f"<div style='background-image:url(data:image/jpg;base64,{encoded_bg});background-size:cover;height:100vh;border-radius:10px'></div>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("Background image 'loginbg.jpg' not found.")

    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("## Welcome Back!")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            col1, col2, col3 = st.columns([1, 1.5, 1.5])
            with col2:
                login_btn = st.form_submit_button("Login")
            with col3:
                signup_btn = st.form_submit_button("Sign Up")

            if login_btn:
                if not email or not password:
                    st.warning("Please enter both email and password.")
                elif authenticate_user(email, password):
                    otp = str(random.randint(100000, 999999))
                    st.session_state.temp_otp = otp
                    st.session_state.temp_email = email

                    if send_otp_email(email, otp):
                        st.success("Password correct! OTP sent to your email.")
                        st.session_state.page = "otp_verify"
                    else:
                        st.error("Failed to send OTP. Try again later.")
                else:
                    st.error("Incorrect email or password!")

            if signup_btn:
                st.session_state.page = "signup"

        st.markdown('</div>', unsafe_allow_html=True)

# OTP Verification Page
def otp_verification_page():
    st.title("OTP Verification")
    st.markdown("Enter the 6-digit OTP sent to your email.")

    if "temp_otp" not in st.session_state:
        st.warning("Session expired. Please login again.")
        if st.button("Back to Login"):
            st.session_state.page = "login"
        return

    user_otp = st.text_input("OTP", max_chars=6)

    if st.button("Verify OTP"):
        if user_otp == st.session_state.get("temp_otp"):
            st.success("✅ OTP verified! You're logged in.")
            st.session_state.page = "climate"
        else:
            st.error("❌ Incorrect OTP. Please try again.")
