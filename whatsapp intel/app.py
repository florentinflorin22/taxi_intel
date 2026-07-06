import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS pentru un design "Pro" - Chenare fixe sus
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    /* Grid 2x2 fixat sus */
    .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    div.stButton > button { width: 100%; height: 50px; border-radius: 8px; border: 1px solid #333; background: #111; color: white; font-weight: bold; }
    div.stButton > button:hover { border-color: #2ecc71; }
    /* Chat input stilizat */
    .stChatInput { margin-bottom: 20px; }
    .box { background: #111; padding: 12px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# Inițializare memorie comună
if 'db' not in st.session_state: st.session_state.db = []
if 'page' not in st.session_state: st.session_state.page = 'CHAT'

# 1. HEADER & LOGO (Opțional)
st.markdown("<h2 style='text-align: center;'>TAXI INTEL</h2>", unsafe_allow_html=True)

# 2. CHENARELE (BUTOANELE) FIXE SUS
st.markdown('<div class="btn-grid">', unsafe_allow_html=True)
if st.button("💬 CHAT"): st.session_state.page = 'CHAT'
if st.button("🚆 STATIONS"): st.session_state.page = 'STATIONS'
if st.button("✈️ LCY"): st.session_state.page = 'LCY'
if st.button("✈️ LHR"): st.session_state.page = 'LHR'
st.markdown('</div>', unsafe_allow_html=True)

# 3. CHAT INPUT (STĂ SUS)
if st.session_state.page == 'CHAT':
    user_input = st.chat_input("Write a message...")
    if user_input:
        st.session_state.db.append(user_input.upper())
        st.rerun()

# 4. CONȚINUTUL (MESAJUL SAU DATELE)
st.markdown("---")

if st.session_state.page == 'CHAT':
    for msg in reversed(st.session_state.db):
        st.markdown(f'<div class="box">{msg}</div>', unsafe_allow_html=True)
else:
    st.info(f"LIVE DATA FOR {st.session_state.page} (Updating...)")
