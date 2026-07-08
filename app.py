import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="centered")

# Funcție pentru logo
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return ""

logo_base64 = get_image_base64("logo.png")

# CSS pentru un design curat pe mobil
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .header-bar { display: flex; align-items: center; padding: 10px; border-bottom: 2px solid #2ecc71; margin-bottom: 20px; }
    .logo-box { width: 40px; height: 40px; margin-right: 15px; }
    div.stButton > button { width: 100%; border-radius: 8px; border: 1px solid #2ecc71; background: #111; color: #fff; }
    div.stButton > button:hover { background: #2ecc71; color: #000; }
</style>
""", unsafe_allow_html=True)

# 1. HEADER (Logo sus)
st.markdown(f'<div class="header-bar"><img src="data:image/png;base64,{logo_base64}" class="logo-box"> <h3>TAXI INTEL</h3></div>', unsafe_allow_html=True)

# 2. MENIU BUTOANE (Grid 2x2)
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT"): st.session_state.activ = 'CHAT'
if c2.button("TRAINS"): st.session_state.activ = 'TRAINS'
if c3.button("LCY"): st.session_state.activ = 'LCY'
if c4.button("LHR"): st.session_state.activ = 'LHR'

st.markdown("---")

# 3. CONȚINUT DINAMIC (Fereastra care se schimbă)
st.subheader(f"Pagina: {st.session_state.activ}")

if st.session_state.activ == 'CHAT':
    if "msgs" not in st.session_state: st.session_state.msgs = []
    text = st.chat_input("Scrie mesaj...")
    if text: st.session_state.msgs.append(text)
    for m in st.session_state.msgs: st.write(f"💬 {m}")

elif st.session_state.activ == 'TRAINS':
    st.write("📋 Detalii actualizate pentru trenuri...")
    # Aici vei adăuga informațiile despre trenuri

elif st.session_state.activ == 'LCY':
    st.write("✈️ Stare zboruri LCY...")

elif st.session_state.activ == 'LHR':
    st.write("✈️ Stare zboruri LHR...")
