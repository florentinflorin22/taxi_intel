import streamlit as st
import urllib.request
import json

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS pentru butoane tip pătrat și stilizare
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    /* Butoane pătrate */
    div.stButton > button { width: 100%; height: 80px; font-weight: bold; background-color: #1a1a1a; 
                            color: #fff; border: 1px solid #333; border-radius: 10px; font-size: 12px; }
    div.stButton > button:hover { background-color: #2ecc71; }
    /* Stil pentru activ */
    .active-btn { background-color: #2ecc71 !important; }
    .box { background: #0a0a0a; padding: 15px; border-radius: 8px; border-left: 4px solid #2ecc71; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# Inițializare stare
if 'page' not in st.session_state: st.session_state.page = 'CHAT'

# Grid 2x2 pentru 4 butoane
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if col1.button("CHAT"): st.session_state.page = 'CHAT'
if col2.button("STATIONS"): st.session_state.page = 'STATIONS'
if col3.button("LCY AIRPORT"): st.session_state.page = 'LCY'
if col4.button("HEATHROW"): st.session_state.page = 'LHR'

# LOGICĂ CONȚINUT
st.markdown("---")

if st.session_state.page == 'CHAT':
    st.subheader("DRIVER CHAT")
    if 'db' not in st.session_state: st.session_state.db = []
    user_input = st.chat_input("Message...")
    if user_input: st.session_state.db.append(user_input.upper())
    for msg in st.session_state.db:
        st.markdown(f'<div class="box" style="border-left-color:#3498db;">{msg}</div>', unsafe_allow_html=True)

elif st.session_state.page == 'STATIONS':
    st.subheader("TRAIN STATIONS")
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC"}
    for name, code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
            with urllib.request.urlopen(url, timeout=1) as res:
                t = json.loads(res.read().decode()).get("trainServices", [])[0]
                st.markdown(f'<div class="box"><b>{name}</b><br>🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}</div>', unsafe_allow_html=True)
        except: continue

elif st.session_state.page == 'LCY':
    st.subheader("CITY AIRPORT (LCY)")
    st.markdown('<div class="box">✈️ FLIGHTS MONITORING...</div>', unsafe_allow_html=True)

elif st.session_state.page == 'LHR':
    st.subheader("HEATHROW (LHR)")
    st.markdown('<div class="box">✈️ TERMINAL ARRIVALS LIVE...</div>', unsafe_allow_html=True)
