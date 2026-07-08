import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# Funcție pentru logo
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return ""

logo_base64 = get_image_base64("logo.png")

# CSS pentru Header Fix + Butoane
st.markdown(f"""
<style>
    .stApp {{ background-color: #000000 !important; }}
    .header-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 130px;
        background: #000000; z-index: 999; padding: 10px; border-bottom: 2px solid #2ecc71;
    }}
    .logo-img {{ width: 50px; height: 50px; border-radius: 50%; float: left; margin-right: 10px; }}
    .content-area {{ margin-top: 140px; }} /* Spațiu ca să nu se suprapună */
</style>
""", unsafe_allow_html=True)

# Afișare Header Fix
st.markdown(f"""
<div class="header-container">
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    <div style="color:white; font-size:18px; font-weight:bold;">TAXI INTEL</div>
    <div style="color:#2ecc71; font-size:12px;">● LONDON LIVE FEED</div>
</div>
""", unsafe_allow_html=True)

# 5. ZONA DE CONȚINUT (Aici încep butoanele și chat-ul)
st.markdown('<div class="content-area"></div>', unsafe_allow_html=True)

# Butoane 2x2
if 'page' not in st.session_state: st.session_state.page = 'CHAT'
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if col1.button("CHAT", use_container_width=True): st.session_state.page = 'CHAT'
if col2.button("TRAINS", use_container_width=True): st.session_state.page = 'TRAINS'
if col3.button("LCY", use_container_width=True): st.session_state.page = 'LCY'
if col4.button("LHR", use_container_width=True): st.session_state.page = 'LHR'

st.markdown("---")

# Logica de afișare
if st.session_state.page == 'CHAT':
    if "messages" not in st.session_state: st.session_state.messages = []
    user_input = st.chat_input("Scrie ceva...")
    if user_input: st.session_state.messages.append(user_input)
    for msg in st.session_state.messages: st.write(f"💬 {msg}")
else:
    st.info(f"Pagina {st.session_state.page} este în lucru.")
