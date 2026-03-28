import streamlit as st
import random
import time
import pandas as pd

# 1. Page Config
st.set_page_config(
    page_title="Astraeus AI | Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Styling (Dark Mode Space Theme)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-family: 'Courier New', monospace; }
    .stAlert { border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State (The "Brain")
if 'o2' not in st.session_state:
    st.session_state.o2 = 100.0
    st.session_state.h2o = 100.0
    st.session_state.history = []

# 4. Sidebar Controls
with st.sidebar:
    st.title("🛰️ Astraeus AI")
    st.write("v2.0 Global Access")
    crew = st.slider("Crew Members", 1, 12, 4)
    activity = st.select_slider("Activity Level", ["Sleep", "Routine", "Training", "EVA"])
    if st.button("♻️ Reset Life Support"):
        st.session_state.o2 = 100.0
        st.session_state.h2o = 100.0
        st.session_state.history = []

# 5. Simulation Logic
rate_map = {"Sleep": 0.02, "Routine": 0.05, "Training": 0.12, "EVA": 0.25}
usage = rate_map[activity] * crew
st.session_state.o2 = max(0, st.session_state.o2 - usage)
st.session_state.h2o = max(0, st.session_state.h2o - (usage * 0.4))

# Track History for Graphs
st.session_state.history.append(st.session_state.o2)
if len(st.session_state.history) > 20: st.session_state.history.pop(0)

# 6. UI Layout (Responsive)
st.header("🔴 Live Telemetry")

col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Oxygen Reserve", f"{st.session_state.o2:.1f}%", f"-{usage}/tick")
col2.metric("Water Supply", f"{st.session_state.h2o:.1f}L", f"-{usage*0.4:.2f}/tick")
col3.metric("CO2 Levels", f"{0.03 + (100-st.session_state.o2)*0.01:.2f}%", "Rising")

# 7. AI Analysis Card
st.subheader("🧠 Astraeus AI Intelligence")
o2_time = st.session_state.o2 / (usage + 0.001)

if o2_time > 20:
    st.success(f"✅ STATUS: Optimal. Systems projecting {int(o2_time)} hours of life support.")
elif o2_time > 10:
    st.warning(f"⚠️ ADVISORY: Oxygen depletion in {int(o2_time)} hours. Reduce activity.")
else:
    st.error(f"🚨 CRITICAL: Immediate action required. Life support ends in {o2_time:.1f}h.")

# 8. Visual Graph (Looks great on Windows/Mac)
st.line_chart(st.session_state.history)

# 9. Auto-Refresh (Runs every 2 seconds)
time.sleep(2)
st.rerun()
