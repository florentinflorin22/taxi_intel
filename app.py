import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="centered")

def get_image_base64(path):
    try:
        with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return ""

logo_base64 = get_image_base64("logo.png")

# 1. CSS - Observă acoladele duble {{ }} pentru a evita eroarea
st.markdown(f"""
<style>
    .stApp {{ background-color: #000000; }}
    .header-box {{ display: flex; align-items: center; gap: 15px; border-bottom: 2px solid #2ecc71; padding-bottom: 10px; margin-bottom: 20px; }}
    .logo-img {{ width: 50px; height: 50px; border-radius: 50%; }}
    h2 {{ margin: 0; color: white; }}
</style>
""", unsafe_allow_html=True)

# 2. HEADER
st.markdown(f"""
<div class="header-box">
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    <h2>TAXI INTEL</h2>
</div>
""", unsafe_allow_html=True)

# 3. BUTOANE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if col1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if col2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if col3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if col4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.markdown("<br>", unsafe_allow_html=True)

# 4. PAGINI
st.subheader(f"Pagina: {st.session_state.activ}")

if st.session_state.activ == 'CHAT':
    if "msgs" not in st.session_state: st.session_state.msgs = []
    text = st.chat_input("Scrie mesaj...")
    if text: st.session_state.msgs.append(text)
    for m in st.session_state.msgs: st.write(f"💬 {m}")
else:
    st.info(f"Detalii pentru {st.session_state.activ}...")
