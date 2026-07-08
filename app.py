import streamlit as st
import base64

st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS simplu doar pentru aspect
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white; }
</style>
""", unsafe_allow_html=True)

# 1. HEADER (Simplu, fără HTML complicat)
st.title("TAXI INTEL")

# 2. BUTOANE (Grid stabil)
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# 3. ZONA DE CHAT (Aici e secretul: folosim un container cu înălțime fixă)
# Astfel, butoanele rămân sus, iar chat-ul se derulează în interiorul acestui container
chat_container = st.container(height=500) 

with chat_container:
    if st.session_state.activ == 'CHAT':
        if "msgs" not in st.session_state: st.session_state.msgs = []
        for m in st.session_state.msgs: st.write(f"💬 {m}")
    else:
        st.info(f"Detalii pentru {st.session_state.activ}")

# 4. INPUT (Rămâne jos, fixat de Streamlit)
text = st.chat_input("Scrie mesaj...")
if text:
    st.session_state.msgs.append(text)
    st.rerun() # Reîmprospătăm ca să apară mesajul imediat
