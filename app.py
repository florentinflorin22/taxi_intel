import streamlit as st
from datetime import datetime, timedelta

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel London", layout="wide")

# 2. CSS AVANSAT - London Transport Style
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #fff; }
    .station-card {
        background: #1a1a1a; padding: 15px; border-radius: 8px;
        border-left: 5px solid #FFD700; margin-bottom: 10px;
    }
    .station-name { font-weight: bold; color: #FFD700; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

# 3. DATE CU GĂRI ȘI AEROPORTURI
london_hubs = {
    "Stations": [
        {"name": "London Waterloo", "status": "Busy", "eta": "16:30"},
        {"name": "London Victoria", "status": "Moderate", "eta": "16:35"},
        {"name": "Paddington", "status": "High Volume", "eta": "16:40"},
        {"name": "Kings Cross", "status": "Active", "eta": "16:50"}
    ],
    "Airports": [
        {"name": "Heathrow (LHR)", "origin": "JFK", "eta": "16:45"},
        {"name": "Gatwick (LGW)", "origin": "DXB", "eta": "17:05"}
    ]
}

# 4. SIDEBAR - SELECTOR HUB
with st.sidebar:
    st.title("📍 LONDON HUB")
    category = st.radio("Select Zone:", ["Stations", "Airports"])
    st.divider()
    st.info("Monitorizează fluxul de pasageri pentru a identifica zonele cu potențial maxim de cursă.")

# 5. LOGICĂ AFIȘARE
st.title(f"Live Status: {category}")

cols = st.columns(2)
for i, item in enumerate(london_hubs[category]):
    with cols[i % 2]:
        if category == "Stations":
            st.markdown(f"""
                <div class="station-card">
                    <div class="station-name">{item['name']}</div>
                    <p>Status: {item['status']}<br>Next peak: {item['eta']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="station-card">
                    <div class="station-name">{item['name']}</div>
                    <p>Origin: {item['origin']}<br>ETA: {item['eta']}</p>
                </div>
            """, unsafe_allow_html=True)
