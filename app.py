import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="wide")

def get_image_base64(path):
    try:
        with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return ""

logo_base64 = get_image_base64("logo.png")

# CSS pentru eliminarea spațiilor albe inutile
st.markdown("""
<style>
    /* Ascunde tot ce este standard Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: #000 !important; padding: 0 !important;}
    
    /* Container fix, fără margini */
    .css-1544g2n {padding: 0 !important;} 
    
    /* Butoane stilizate strict */
    div.stButton > button {
        height: 60px !important;
        font-weight: bold;
        border: 2px solid #2ecc71 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Compact
col_img, col_title = st.columns([1, 4])
with col_img:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" style="width:50px; border-radius:50%">', unsafe_allow_html=True)
with col_title:
    st.markdown("<h2 style='margin:0'>TAXI INTEL</h2>", unsafe_allow_html=True)

st.divider()

# Butoane compacte (Grid)
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# Zona de conținut (începe imediat sub butoane)
if st.session_state.activ == 'CHAT':
    if "msgs" not in st.session_state: st.session_state.msgs = []
    text = st.chat_input("Scrie mesaj...")
    if text: st.session_state.msgs.append(text)
    for m in st.session_state.msgs: st.write(f"💬 {m}")
else:
    st.info(f"Detalii pentru: {st.session_state.activ}")
