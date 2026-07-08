import streamlit as st
import requests

# 1. LOGICĂ DE VITEZĂ (Caching - pusă sus de tot)
@st.cache_data(ttl=900)
def get_trains_live():
    # Timeout setat la 2 secunde pentru a preveni blocarea aplicației
    try:
        # Exemplu: aici va veni URL-ul de la API-ul tău de trenuri
        # response = requests.get("https://api...", timeout=2)
        # return response.json()
        
        # Date simulate pentru testare imediată
        return [
            {"nume": "Heathrow Express", "vagoane": 8, "status": "On Time"},
            {"nume": "Gatwick Express", "vagoane": 10, "status": "On Time"},
            {"nume": "Stansted Express", "vagoane": 8, "status": "Delayed"}
        ]
    except:
        return []

# 2. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel", layout="centered")

# 3. CSS OPTIMIZAT
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { 
        border-radius: 10px !important; border: 1px solid #2ecc71 !important; 
        background: #111 !important; color: white !important; height: 50px;
    }
    .train-card { background:#111; padding:12px; border-radius:8px; border-left: 6px solid #f1c40f; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

# 4. HEADER
st.title("TAXI INTEL")

# 5. INITIALIZARE STARE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'
if 'msgs' not in st.session_state: st.session_state.msgs = []

# 6. MENIU
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)
if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'
st.divider()

# 7. LOGICĂ CONȚINUT
if st.session_state.activ == 'CHAT':
    with st.container(height=400):
        for m in st.session_state.msgs[-20:]: # Limităm la ultimele 20 pentru viteză
            with st.chat_message("user"): st.write(m)
    text = st.chat_input("Scrie mesaj...")
    if text:
        st.session_state.msgs.append(text)
        st.rerun()

elif st.session_state.activ == 'TRAINS':
    st.markdown("### 🚂 Trenuri (8+ Vagoane)")
    trenuri = get_trains_live() # Apelăm funcția cache-uită
    for t in trenuri:
        if t['vagoane'] >= 8:
            st.markdown(f"""
                <div class="train-card">
                    <strong>{t['nume']}</strong><br>
                    Vagoane: {t['vagoane']} | Status: <span style="color:#2ecc71;">{t['status']}</span>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.activ in ['LCY', 'LHR']:
    st.markdown(f"### ✈️ {st.session_state.activ} Status")
    st.info("Monitorizare activă.")

# 8. AUTO-REFRESH
st.markdown('<meta http-equiv="refresh" content="900">', unsafe_allow_html=True)
