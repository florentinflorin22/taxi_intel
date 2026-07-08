import streamlit as st
import requests

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel", layout="centered")

# 2. CSS PENTRU ASPECT MOBIL
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { 
        border-radius: 10px !important; 
        border: 1px solid #2ecc71 !important; 
        background: #111 !important; 
        color: white !important; 
        height: 50px;
    }
    div.stButton > button:hover { background: #2ecc71 !important; color: black !important; }
    .train-card { background:#111; padding:12px; border-radius:8px; border-left: 6px solid #f1c40f; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.title("TAXI INTEL")

# 4. INITIALIZARE STARE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'
if 'msgs' not in st.session_state: st.session_state.msgs = []

# 5. MENIU BUTOANE
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# 6. LOGICĂ CONȚINUT
if st.session_state.activ == 'CHAT':
    with st.container(height=400):
        for m in st.session_state.msgs:
            with st.chat_message("user"):
                st.write(m)
    text = st.chat_input("Scrie mesaj...")
    if text:
        st.session_state.msgs.append(text)
        st.rerun()

elif st.session_state.activ == 'TRAINS':
    st.markdown("### 🚂 Trenuri Express (8+ Vagoane)")
    
    # Lista simulată (Înlocuiește cu un apel API real către National Rail Darwin)
    trenuri_live = [
        {"nume": "Heathrow Express", "vagoane": 8, "status": "On Time"},
        {"nume": "Gatwick Express", "vagoane": 10, "status": "On Time"},
        {"nume": "Southeastern Highspeed", "vagoane": 6, "status": "On Time"}, # Acesta va fi filtrat
        {"nume": "Stansted Express", "vagoane": 8, "status": "Delayed"}
    ]
    
    for t in trenuri_live:
        # Filtrare: afișăm doar dacă au 8+ vagoane
        if t['vagoane'] >= 8:
            st.markdown(f"""
                <div class="train-card">
                    <strong>{t['nume']}</strong><br>
                    Compunere: {t['vagoane']} vagoane | Status: <span style="color:#2ecc71;">{t['status']}</span>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.activ == 'LCY':
    st.markdown("### ✈️ LCY Airport Live")
    st.info("Monitorizare activă pentru London City Airport.")

elif st.session_state.activ == 'LHR':
    st.markdown("### ✈️ LHR Airport Live")
    st.info("Monitorizare activă pentru Heathrow Airport.")

# 7. AUTO-REFRESH (la fiecare 15 minute = 900 secunde)
st.markdown('<meta http-equiv="refresh" content="900">', unsafe_allow_html=True)
