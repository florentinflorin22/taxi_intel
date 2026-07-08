import streamlit as st
from datetime import datetime

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Pro", layout="wide")

# 2. CSS AVANSAT (Control Panel Style)
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #fff; }
    .card-urgent { border-left: 5px solid #ff4b4b !important; }
    .card-normal { border-left: 5px solid #00ff9d !important; }
    .data-card {
        background: #151515; padding: 20px; border-radius: 15px; margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .big-font { font-size: 24px; font-weight: bold; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR - CONTROL PANEL
with st.sidebar:
    st.header("⚙️ Control Panel")
    min_capacity = st.slider("Min. Carriages (Capacity)", 4, 12, 8)
    st.divider()
    show_delays_only = st.toggle("Show Delays Only")

# 4. LOGICA DATELOR (Simulare)
data = [
    {"name": "Heathrow Express", "type": "Train", "eta": "16:45", "cap": 9, "status": "On Time"},
    {"name": "Gatwick Express", "type": "Train", "eta": "17:10", "cap": 7, "status": "Delayed"},
    {"name": "LHR Arrivals", "type": "Airport", "eta": "17:20", "cap": 12, "status": "Busy"}
]

# 5. DASHBOARD PRINCIPAL
st.title("Taxi Intel Pro")
st.metric("System Status", "Live", delta="Connected")

cols = st.columns(3)
for i, item in enumerate(data):
    # Filtrare
    if item["cap"] < min_capacity: continue
    if show_delays_only and item["status"] != "Delayed": continue
    
    css_class = "card-urgent" if item["status"] == "Delayed" else "card-normal"
    
    with cols[i % 3]:
        st.markdown(f"""
            <div class="data-card {css_class}">
                <div style="color: #888;">{item['type']}</div>
                <div class="big-font">{item['name']}</div>
                <p>ETA: {item['eta']} | Cap: {item['cap']}</p>
                <b>{item['status']}</b>
            </div>
        """, unsafe_allow_html=True)
