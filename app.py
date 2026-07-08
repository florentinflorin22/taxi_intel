import streamlit as st
from datetime import datetime

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel London", layout="wide")

# 2. CSS PROFESIONAL
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; }
    .station-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #111111 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 12px;
        border: 1px solid #333;
    }
    .station-name { font-weight: bold; color: #FFD700; font-size: 1.1em; }
    .status-text { color: #888; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# 3. DATE - GĂRI + LONDON CITY AIRPORT
hubs = [
    "London Waterloo", "London Victoria", "Paddington", "Kings Cross", 
    "Euston", "St Pancras International", "London Bridge", "Liverpool Street", 
    "Charing Cross", "London City Airport (LCY)"
]

# 4. SIDEBAR
with st.sidebar:
    st.title("📍 LONDON HUBS")
    st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    selected_hub = st.selectbox("Select Location to Monitor:", hubs)
    st.info("Monitor real-time demand for these 10 key London transport hubs.")

# 5. LOGICĂ AFIȘARE
st.title(f"Live Status: {selected_hub}")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
        <div class="station-card">
            <div class="station-name">{selected_hub}</div>
            <p class="status-text">Operational Status: <b>Active</b></p>
            <p class="status-text">Current Demand: <b>High</b></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Next Expected Peaks (Next 30m)")
    # Simulare date
    for i in range(1, 4):
        st.markdown(f"""
            <div class="station-card">
                <div class="station-name">Peak Expected in {i*10} minutes</div>
                <p class="status-text">Estimated passenger outflow: <b>{50 + (i*25)} pax</b></p>
            </div>
        """, unsafe_allow_html=True)
