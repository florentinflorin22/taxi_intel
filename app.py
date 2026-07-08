import streamlit as st
from datetime import datetime

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Pro", layout="centered")

# 2. CSS PROFESIONAL
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #111; border-right: 1px solid #333; }
    .data-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #111111 100%);
        padding: 18px;
        border-radius: 12px;
        border-left: 4px solid #FFD700;
        margin-bottom: 15px;
        border: 1px solid #222;
    }
    .metric-title { color: #888; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 1.4em; color: #fff; font-weight: bold; }
    .status-pill { background: #1a3a2a; color: #2ecc71; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; float: right; }
</style>
""", unsafe_allow_html=True)

# 3. DATE LIVE (Trenuri + Aeroporturi)
transport_data = {
    "TRAINS": [
        {"name": "Heathrow Express", "status": "On Time", "eta": "16:45"},
        {"name": "Gatwick Express", "status": "On Time", "eta": "17:10"}
    ],
    "AIRPORTS": [
        {"name": "London City (LCY)", "status": "Active", "delay": "None", "eta": "16:55"},
        {"name": "Heathrow (LHR)", "status": "Busy", "delay": "15 min", "eta": "17:20"}
    ]
}

# 4. SIDEBAR
with st.sidebar:
    st.title("TAXI INTEL")
    st.caption(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    if st.button("TRAINS"): st.session_state.activ = 'TRAINS'
    if st.button("AIRPORTS"): st.session_state.activ = 'AIRPORTS'

# 5. LOGICĂ AFIȘARE
if 'activ' not in st.session_state: st.session_state.activ = 'TRAINS'

if st.session_state.activ == 'TRAINS':
    st.subheader("🚂 Train Monitoring")
    for t in transport_data["TRAINS"]:
        st.markdown(f"""
            <div class="data-card">
                <span class="status-pill">{t["status"]}</span>
                <div class="metric-title">{t["name"]}</div>
                <div class="metric-value">ETA: {t["eta"]}</div>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.activ == 'AIRPORTS':
    st.subheader("✈️ Airport Arrivals")
    for a in transport_data["AIRPORTS"]:
        st.markdown(f"""
            <div class="data-card">
                <span class="status-pill">{a["status"]}</span>
                <div class="metric-title">{a["name"]}</div>
                <div class="metric-value">ETA: {a["eta"]}</div>
                <div style="font-size: 0.8em; color: #f39c12;">Delay: {a["delay"]}</div>
            </div>
        """, unsafe_allow_html=True)
