import streamlit as st
import datetime
import re
import sqlite3
import hashlib

# 🔧 Initialize DB and create table
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            country TEXT NOT NULL,
            gender TEXT NOT NULL,
            subscribed BOOLEAN NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 🔐 Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 💾 Insert new user into DB
def insert_user(email, password, first_name, last_name, dob, country, gender, subscribed):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password, first_name, last_name, date_of_birth, country, gender, subscribed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, hash_password(password), first_name, last_name, dob, country, gender, subscribed))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# 🌍 Main signup UI
def signup_page():
    init_db()  # Initialize database on load

    st.set_page_config(page_title="Join Us - Climate Change Awareness", layout="centered")

    # Styling
    st.markdown("""
        <style>
        .stApp {
            background-color: black;
            color: white;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div > div,
        .stDateInput > div > input,
        .stRadio > div > label,
        .stCheckbox > div > label {
            background-color: #333333;
            color: white;
        }
        .stButton > button {
            background-color: green;
            color: white;
        }
        .error-text {
            color: red;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🔙 Back to Login"):
        st.session_state.page = "login"

    st.title("🌱 Join the Climate Change Awareness Movement")
    st.markdown("Create your account to get updates, participate in events, and contribute to a greener planet.")

    with st.form("signup_form"):
        email = st.text_input("Email address")
        if email and not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            st.markdown('<p class="error-text">Please enter a valid email address.</p>', unsafe_allow_html=True)

        password = st.text_input("Password", type="password")
        if password and not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            st.markdown('<p class="error-text">Password must be at least 8 characters long, include a number, and a special character.</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")

        dob = st.date_input("Date of Birth", value=datetime.date(2000, 1, 1),
                            help="Help us celebrate your birthday with a green surprise!")

        countries = ["India", "United States", "Germany", "Brazil", "Australia", "Other"]
        selected_country = st.selectbox("Country", countries, index=None)

        gender = st.radio("Gender", ["Male", "Female", "Other"], index=None)

        subscribe = st.checkbox("Sign me up for climate news, events, and sustainability tips")

        st.markdown("By creating an account, you agree to our [Privacy Policy](#) and [Terms of Use](#).")

        submit = st.form_submit_button("🌍 JOIN US")

        if submit:
            if not (email and password and first_name and last_name and selected_country and gender):
                st.warning("Please complete all required fields.")
            else:
                success = insert_user(email, password, first_name, last_name, dob, selected_country, gender, subscribe)
                if success:
                    st.success("Welcome! You're now part of the Climate Change Awareness community 🌍")
                    st.session_state.page = "climate"
                else:
                    st.error("This email is already registered. Try logging in instead.")

    st.markdown("---")
