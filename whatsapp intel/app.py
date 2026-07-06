import streamlit as st
import urllib.request
import json

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS cu butoane active și stilizare pentru 9 gări + Aeroporturi
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    /* Stil buton activ */
    .active-btn { background-color: #2ecc71 !important; color: white !important; border: none !important; }
    div.stButton > button { width: 100%; height: 50px; font-weight: bold; background-color: #1a1a1a; color: #2ecc71; border: 1px solid #2ecc71; }
    .train-box { background: #0a0a0a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 4px solid #2ecc71; }
    .chat-box { background: #1a1a1a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 4px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# Memorie
if 'page' not in st.session_state: st.session_state.page = 'TRAINS'
if 'db' not in st.session_state: st.session_state.db = []

# Meniu cu evidențierea paginii active
c1, c2 = st.columns(2)
if c1.button("CHAT", type="primary" if st.session_state.page == 'CHAT' else "secondary"): 
    st.session_state.page = 'CHAT'; st.rerun()
if c2.button("TRAINS & AIRPORTS", type="primary" if st.session_state.page == 'TRAINS' else "secondary"): 
    st.session_state.page = 'TRAINS'; st.rerun()

# LOGICĂ
if st.session_state.page == 'CHAT':
    user_input = st.chat_input("Type update...")
    if user_input: st.session_state.db.append(user_input.upper())
    for msg in st.session_state.db:
        st.markdown(f'<div class="chat-box">{msg}</div>', unsafe_allow_html=True)

else:
    # Lista completă: 9 Gări + 2 Aeroporturi (LCY + LHR)
    # LHR este reprezentat prin Paddington/Express sau gări care deservesc zona
    targets = {
        "ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", 
        "EUSTON": "EUS", "KINGS CROSS": "KGX", "WATERLOO": "WAT", 
        "LONDON BRIDGE": "LBG", "LIVERPOOL ST": "LST", "CHARING CROSS": "CHX",
        "CITY AIRPORT": "LCY", "HEATHROW": "PAD"
    }
    
    for name, code in targets.items():
        try:
            # Pentru aeroporturi, folosim logica de simulare sau sursă externă
            if code == "LCY":
                st.markdown(f'<div class="train-box" style="border-left-color:#3498db;"><b>CITY AIRPORT</b><br>✈️ BUSY (CHECK LIVE)</div>', unsafe_allow_html=True)
            elif code == "PAD" and name == "HEATHROW":
                st.markdown(f'<div class="train-box" style="border-left-color:#3498db;"><b>HEATHROW (via PAD)</b><br>🚆 EXPRESS SERVICE</div>', unsafe_allow_html=True)
            else:
                url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
                with urllib.request.urlopen(url, timeout=1) as res:
                    t = json.loads(res.read().decode()).get("trainServices", [])[0]
                    st.markdown(f"""
                        <div class="train-box">
                            <div style="font-weight:bold; color:#2ecc71;">{name}</div>
                            <div>🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}</div>
                        </div>
                    """, unsafe_allow_html=True)
        except: continue
