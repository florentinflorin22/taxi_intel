import streamlit as st
from datetime import datetime

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Pro", layout="centered")

# 2. CSS PROFESIONAL - Stil Dashboard
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

# 3. DATE CU ORA SOSIRII (ETA)
transport_data = {
    "TRAINS": [
        {"name": "Heathrow Express", "capacity": 8, "status": "On Time", "eta": "16:45"},
        {"name": "Gatwick Express", "capacity": 10, "status": "On Time", "eta": "17:10"},
        {"name": "Stansted Express", "capacity": 8, "status": "Delayed", "eta": "17:30"}
    ]
}

# 4. SIDEBAR
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067403.png", width=60) # Logo sugestiv
    st.title("TAXI INTEL")
    st.caption(f"Update: {datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    if st.button("CHAT"): st.session_state.activ = 'CHAT'
    if st.button("TRAINS"): st.session_state.activ = 'TRAINS'

# 5. LOGICĂ AFIȘARE PROFESIONALĂ
if 'activ' not in st.session_state: st.session_state.activ = 'TRAINS'

if st.session_state.activ == 'TRAINS':
    st.subheader("🚂 Live Train Arrivals")
    for train in transport_data["TRAINS"]:
        if train["capacity"] >= 8:
            st.markdown(f"""
                <div class="data-card">
                    <span class="status-pill">{train["status"]}</span>
                    <div class="metric-title">{train["name"]}</div>
                    <div class="metric-value">ETA: {train["eta"]}</div>
                    <div style="font-size: 0.8em; color: #555;">Capacity: {train["capacity"]} carriages</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.write("### AI Assistant")
    st.info("System ready for your input.")
