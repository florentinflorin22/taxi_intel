import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS PRO - DESIGN APP-LIKE
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    /* Header Logo */
    .logo-container { text-align: center; padding: 20px 0; }
    /* Grid butoane */
    .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    div.stButton > button { width: 100%; height: 60px; border-radius: 10px; border: 1px solid #333; background: #111; color: white; font-weight: bold; }
    div.stButton > button:hover { border-color: #2ecc71; }
    /* Chat fixat jos */
    .stChatInput { position: fixed; bottom: 20px; width: 95%; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

# Logo (încarcă logo.png din folder)
def get_image_base64(path):
    try:
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_image_base64("logo.png")
if logo_b64:
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{logo_b64}" width="120"><h2>TAXI INTEL</h2></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="logo-container"><h2>TAXI INTEL</h2></div>', unsafe_allow_html=True)

# Grid Butoane
if 'page' not in st.session_state: st.session_state.page = 'CHAT'
st.markdown('<div class="btn-grid">', unsafe_allow_html=True)
if st.button("💬 CHAT"): st.session_state.page = 'CHAT'
if st.button("🚆 STATIONS"): st.session_state.page = 'STATIONS'
if st.button("✈️ LCY"): st.session_state.page = 'LCY'
if st.button("✈️ LHR"): st.session_state.page = 'LHR'
st.markdown('</div>', unsafe_allow_html=True)

# Conținut
if st.session_state.page == 'CHAT':
    if 'db' not in st.session_state: st.session_state.db = []
    user_input = st.chat_input("Message...")
    if user_input: st.session_state.db.append(user_input.upper())
    for msg in reversed(st.session_state.db):
        st.markdown(f'<div style="background:#1a1a1a; padding:10px; border-radius:10px; margin:5px 0;">{msg}</div>', unsafe_allow_html=True)
else:
    st.markdown(f"### {st.session_state.page} DATA")
    st.info("Loading live data...")
