import streamlit as st
import urllib.request
import json

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS pentru butoane mari și clare
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { width: 100%; height: 50px; font-weight: bold; background-color: #1a1a1a; color: #2ecc71; border: 1px solid #2ecc71; }
    div.stButton > button:hover { background-color: #2ecc71; color: white; }
    .chat-box { background: #1a1a1a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #3498db; }
    .train-box { background: #0a0a0a; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #2ecc71; }
</style>
""", unsafe_allow_html=True)

# Memorie
if 'page' not in st.session_state: st.session_state.page = 'TRAINS'
if 'db' not in st.session_state: st.session_state.db = []

# Meniu de navigare
c1, c2 = st.columns(2)
if c1.button("CHAT"): st.session_state.page = 'CHAT'
if c2.button("TRAINS"): st.session_state.page = 'TRAINS'

# LOGICĂ PAGINI
if st.session_state.page == 'CHAT':
    user_input = st.chat_input("Type update...")
    if user_input: st.session_state.db.append(user_input.upper())
    for msg in st.session_state.db:
        st.markdown(f'<div class="chat-box">{msg}</div>', unsafe_allow_html=True)

else: # Pagina TRENURI
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC"}
    for name, code in stations.items():
        try:
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
