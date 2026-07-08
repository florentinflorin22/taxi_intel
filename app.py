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

st.markdown("""
<style>
    /* Fixăm Header-ul și Butoanele sus */
    .fixed-header {
        position: sticky; top: 0; background: black; z-index: 999;
        padding-bottom: 10px; border-bottom: 2px solid #2ecc71;
    }
    /* Zona de scroll pentru chat */
    .chat-container {
        height: 60vh; /* Ocupă restul ecranului */
        overflow-y: auto;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 1. Zona care rămâne lipită sus
st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
# Aici pui Header-ul (Logo + Titlu)
# Aici pui Butoanele (c1, c2, c3, c4)
st.markdown('</div>', unsafe_allow_html=True)

# 2. Zona de conținut care scrollează
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# Aici pui logica de afișare (Chat, Trains, etc.)
st.markdown('</div>', unsafe_allow_html=True)

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
