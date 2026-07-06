import streamlit as st
import urllib.request
import json

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS MODERNIZAT
st.markdown("""
<style>
    /* Fundal general negru */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Butoane pătrate stilizate */
    div.stButton > button { 
        width: 100%; height: 80px; font-weight: bold; 
        background-color: #1a1a1a; color: #ffffff; 
        border: 1px solid #333; border-radius: 12px; font-size: 11px;
    }
    div.stButton > button:hover { border-color: #2ecc71; background-color: #0d0d0d; }
    
    /* Box-uri cu aspect de card */
    .box { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a); 
        padding: 15px; border-radius: 12px; 
        border-left: 5px solid #2ecc71; margin-top: 15px; 
        box-shadow: 5px 5px 15px #000;
    }
    
    /* Fortăm culoarea input-ului chat */
    .stChatInput textarea { 
        background-color: #1a1a1a !important; 
        color: white !important; 
        border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Inițializare stare
if 'page' not in st.session_state: st.session_state.page = 'CHAT'

# Grid 2x2 butoane
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if col1.button("CHAT"): st.session_state.page = 'CHAT'
if col2.button("STATIONS"): st.session_state.page = 'STATIONS'
if col3.button("LCY AIRPORT"): st.session_state.page = 'LCY'
if col4.button("HEATHROW"): st.session_state.page = 'LHR'

st.markdown("---")

# LOGICĂ PAGINI
if st.session_state.page == 'CHAT':
    st.markdown("### 💬 DRIVER CHAT")
    if 'db' not in st.session_state: st.session_state.db = []
    
    # Input chat
    user_input = st.chat_input("Write a message...")
    if user_input: st.session_state.db.append(user_input.upper())
    
    for msg in reversed(st.session_state.db):
        st.markdown(f'<div class="box" style="border-left-color:#3498db;">{msg}</div>', unsafe_allow_html=True)

elif st.session_state.page == 'STATIONS':
    st.markdown("### 🚆 TRAIN STATIONS")
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC"}
    for name, code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
            with urllib.request.urlopen(url, timeout=1) as res:
                t = json.loads(res.read().decode()).get("trainServices", [])[0]
                st.markdown(f'<div class="box"><b>{name}</b><br>🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}</div>', unsafe_allow_html=True)
        except: continue

# Pentru restul paginilor (LCY/LHR) poți completa logica similar
elif st.session_state.page == 'LCY':
    st.markdown("### ✈️ CITY AIRPORT (LCY)")
    st.markdown('<div class="box">Monitoring active...</div>', unsafe_allow_html=True)

elif st.session_state.page == 'LHR':
    st.markdown("### ✈️ HEATHROW (LHR)")
    st.markdown('<div class="box">Monitoring active...</div>', unsafe_allow_html=True)
