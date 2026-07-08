import streamlit as st

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel", layout="centered")
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<style>
    /* Forțăm totul să fie pe tot ecranul, fără margini inutile */
    .block-container { 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        padding-top: 1rem !important; 
    }
    /* Să nu avem scroll orizontal pe mobil */
    body { overflow-x: hidden; }
</style>
""", unsafe_allow_html=True)

# 2. CSS PENTRU ASPECT CURAT
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { 
        border-radius: 10px !important; 
        border: 1px solid #2ecc71 !important; 
        background: #111 !important; 
        color: white !important; 
        height: 50px;
    }
    div.stButton > button:hover { background: #2ecc71 !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.title("TAXI INTEL")

# 4. LOGICĂ BUTOANE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'
if 'msgs' not in st.session_state: st.session_state.msgs = []

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# 5. CONȚINUT DINAMIC
if st.session_state.activ == 'CHAT':
    # Container cu scroll pentru mesaje
    with st.container(height=400):
        for m in st.session_state.msgs:
            with st.chat_message("user"):
                st.write(m)
    
    # Input-ul rămâne fix jos
    text = st.chat_input("Scrie mesaj...")
    if text:
        st.session_state.msgs.append(text)
        st.rerun()

elif st.session_state.activ == 'TRAINS':
    st.markdown("### 🚂 Status Trenuri")
    st.info("Aici vor veni datele pentru trenuri.")

elif st.session_state.activ == 'LCY':
    st.markdown("### ✈️ LCY Airport")
    st.info("Aici vor veni datele pentru LCY.")

elif st.session_state.activ == 'LHR':
    st.markdown("### ✈️ LHR Airport")
    st.info("Aici vor veni datele pentru LHR.")
