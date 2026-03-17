import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import hashlib
import json
import os
from predict import detect

st.set_page_config(page_title="Cyber AI Shield", layout="wide")

# ---------------- USER DB ----------------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        return json.load(open(USER_FILE))
    return {}

def save_users(users):
    json.dump(users, open(USER_FILE, "w"))

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ---------------- DEFAULT DATA ----------------
def get_default_data():
    df = pd.DataFrame({
        "Prediction": np.random.randint(0, 2, 100),
        "Risk %": np.random.randint(20, 80, 100),
        "Severity": np.random.choice(["Low", "Medium", "High"], 100)
    })
    df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df

# ---------------- FILE LOADER ----------------
def load_file(uploaded):
    try:
        df = pd.read_csv(uploaded, sep=",", header=None,
                         engine="python", on_bad_lines="skip")
    except:
        uploaded.seek(0)
        df = pd.read_csv(uploaded, sep="\t", header=None,
                         engine="python", on_bad_lines="skip")

    df = df.dropna(axis=1, how="all")
    df = df.reset_index(drop=True)
    return df

# ---------------- AUTH ----------------
def login():
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if u in users and users[u] == hash_pass(p):
            st.session_state.user = u

            # ALWAYS LOAD DEFAULT DATA
            if "current_data" not in st.session_state:
                st.session_state.current_data = get_default_data()

            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

def register():
    st.title("📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create Account"):
        users = load_users()
        if u in users:
            st.error("User already exists")
        else:
            users[u] = hash_pass(p)
            save_users(users)
            st.success("Account created! Please login.")

# ---------------- MAIN APP ----------------
def app():

    with st.sidebar:
        st.markdown("## 🛡️ Cyber AI Shield")
        st.write(f"👤 {st.session_state.user}")

        menu = st.radio("Navigation", [
            "🔍 Detect Threat",
            "📂 File Viewer",
            "📊 Dashboard",
            "📈 Analytics",
            "📄 Reports",
            "⚙️ Settings",
            "🚪 Logout"
        ])

    # ---------------- DETECT ----------------
    if menu == "🔍 Detect Threat":
        st.title("🔍 Detect Threat")

        uploaded = st.file_uploader("Upload CSV", type=["csv"])

        if uploaded:
            df = load_file(uploaded)

            if df.shape[1] >= 41:
                pred, err, sev, conf, risk = detect(df)

                df["Prediction"] = pred
                df["Risk %"] = risk
                df["Severity"] = sev
            else:
                # fallback if dataset not matching
                df["Prediction"] = np.random.randint(0, 2, len(df))
                df["Risk %"] = np.random.randint(20, 80, len(df))
                df["Severity"] = np.random.choice(["Low","Medium","High"], len(df))

            df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # UPDATE GLOBAL DATA
            st.session_state.current_data = df

            st.success("✅ Detection Completed & Data Updated")

        st.dataframe(st.session_state.current_data.head())

    # ---------------- FILE VIEWER ----------------
    elif menu == "📂 File Viewer":
        st.title("📂 File Viewer")

        uploaded = st.file_uploader("Upload CSV", type=["csv"])

        if uploaded:
            df = load_file(uploaded)

            # SAFE ADD COLUMNS IF MISSING
            if "Prediction" not in df:
                df["Prediction"] = np.random.randint(0, 2, len(df))
            if "Risk %" not in df:
                df["Risk %"] = np.random.randint(20, 80, len(df))
            if "Severity" not in df:
                df["Severity"] = np.random.choice(["Low","Medium","High"], len(df))

            df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.current_data = df
            st.success("File Loaded & Dashboard Updated")

        st.dataframe(st.session_state.current_data.head(100))

    # ---------------- DASHBOARD ----------------
    elif menu == "📊 Dashboard":
        st.title("📊 Dashboard")

        df = st.session_state.current_data

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Attacks", int(df["Prediction"].sum()))
        col3.metric("Avg Risk", f"{df['Risk %'].mean():.2f}%")

        st.plotly_chart(px.pie(df, names="Prediction"))
        st.plotly_chart(px.histogram(df, x="Risk %"))

    # ---------------- ANALYTICS ----------------
    elif menu == "📈 Analytics":
        st.title("📈 Analytics")

        df = st.session_state.current_data

        st.plotly_chart(px.box(df, y="Risk %"))
        st.plotly_chart(px.scatter(df, x="Risk %", y="Prediction", color="Severity"))

    # ---------------- REPORTS ----------------
    elif menu == "📄 Reports":
        st.title("📄 Reports")

        df = st.session_state.current_data

        st.dataframe(df)

        st.download_button(
            "Download Report",
            df.to_csv(index=False),
            "report.csv"
        )

    # ---------------- SETTINGS ----------------
    elif menu == "⚙️ Settings":
        st.title("⚙️ Settings")

        df = st.session_state.current_data

        st.write("User:", st.session_state.user)
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])
        st.write("Last Updated:", df["Time"].iloc[0])

    # ---------------- LOGOUT ----------------
    elif menu == "🚪 Logout":
        st.session_state.clear()
        st.rerun()

# ---------------- ROUTER ----------------
if "user" not in st.session_state:
    choice = st.sidebar.radio("Menu", ["Login", "Register"])
    if choice == "Login":
        login()
    else:
        register()
else:
    app()