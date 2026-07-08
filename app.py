import streamlit as st
import base64

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel", layout="centered")

# Funcție logo
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return ""

logo_base64 = get_image_base64("logo.png")

# 2. CSS (Design curat)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .header-box { display: flex; align-items: center; gap: 15px; border-bottom: 2px solid #2ecc71; padding-bottom: 10px; margin-bottom: 20px; }
    .logo-img { width: 50px; height: 50px; border-radius: 50%; }
    h2 { margin: 0; color: white; }
    div.stButton > button { height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white; }
    div.stButton > button:hover { background: #2ecc71; color: black; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown(f"""
<div class="header-box">
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    <h2>TAXI INTEL</h2>
</div>
""", unsafe_allow_html=True)

# 4. LOGICĂ BUTOANE (Inițializare o singură dată)
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# 5. CONȚINUT DINAMIC
if st.session_state.activ == 'CHAT':
    st.markdown("### 💬 Chat Live")
    if "msgs" not in st.session_state: st.session_state.msgs = []
    text = st.chat_input("Scrie mesaj...")
    if text: st.session_state.msgs.append(text)
    for m in st.session_state.msgs: st.write(f"💬 {m}")

elif st.session_state.activ == 'TRAINS':
    st.markdown("### 🚂 Status Trenuri")
    st.info("Aici vor veni datele pentru trenuri.")

elif st.session_state.activ == 'LCY':
    st.markdown("### ✈️ LCY Airport")
    st.info("Aici vor veni datele pentru LCY.")

elif st.session_state.activ == 'LHR':
    st.markdown("### ✈️ LHR Airport")
    st.info("Aici vor veni datele pentru LHR.")
