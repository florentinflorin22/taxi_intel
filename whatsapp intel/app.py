import streamlit as st
import urllib.request
import json
from streamlit_autorefresh import st_autorefresh

# 1. AUTO-REFRESH (Setat la 5 secunde pentru a fi "Live")
st_autorefresh(interval=5000, key="datarefresh")

st.set_page_config(page_title="Taxi Intel", layout="centered")

# 2. CSS FORȚAT pentru butoane 2x2 pe telefon
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    /* Grid forțat pe mobil */
    [data-testid="column"] { width: 50% !important; flex: 1 1 50% !important; }
    div.stButton > button { width: 100%; height: 50px; font-weight: bold; background-color: #1a1a1a; 
                            color: #2ecc71; border: 1px solid #2ecc71; border-radius: 8px; }
    div.stButton > button:hover { background-color: #2ecc71; color: white; }
    .chat-box { background: #1a1a1a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #3498db; }
    .train-box { background: #0a0a0a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #2ecc71; }
</style>
""", unsafe_allow_html=True)

# Inițializare
if 'page' not in st.session_state: st.session_state.page = 'CHAT'
if 'db' not in st.session_state: st.session_state.db = []

# Meniu butoane (2x2 fixat)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if st.button("CHAT"): st.session_state.page = 'CHAT'
with col2:
    if st.button("TRAINS"): st.session_state.page = 'TRAINS'
with col3:
    if st.button("LCY"): st.session_state.page = 'LCY'
with col4:
    if st.button("LHR"): st.session_state.page = 'LHR'

st.markdown("---")

# LOGICĂ
if st.session_state.page == 'CHAT':
    user_input = st.chat_input("Type update...")
    if user_input: st.session_state.db.append(user_input.upper())
    for msg in reversed(st.session_state.db):
        st.markdown(f'<div class="chat-box">{msg}</div>', unsafe_allow_html=True)
elif st.session_state.page == 'TRAINS':
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC"}
    for name, code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
            with urllib.request.urlopen(url, timeout=2) as res:
                t = json.loads(res.read().decode()).get("trainServices", [])[0]
                st.markdown(f'<div class="train-box"><b>{name}</b><br>🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}</div>', unsafe_allow_html=True)
        except: st.markdown(f'<div class="train-box">{name}: Info N/A</div>', unsafe_allow_html=True)
