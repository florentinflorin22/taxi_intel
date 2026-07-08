import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. CODUL HTML/CSS "PIXEL-PERFECT"
# Aici construim exact layout-ul din schița ta
app_html = """
<div style="background-color: black; color: white; height: 100vh; padding: 20px; font-family: sans-serif;">
    <div style="display: flex; align-items: center; border-bottom: 2px solid #2ecc71; padding-bottom: 10px;">
        <div style="width: 50px; height: 50px; background: #333; border-radius: 50%; margin-right: 15px;"></div>
        <h2 style="margin: 0;">TAXI INTEL</h2>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
        <button onclick="parent.postMessage('CHAT', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">CHAT</button>
        <button onclick="parent.postMessage('TRAINS', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">TRAINS</button>
        <button onclick="parent.postMessage('LCY', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">LCY</button>
        <button onclick="parent.postMessage('LHR', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">LHR</button>
    </div>
    
    <div id="content" style="margin-top: 30px; border: 1px solid #333; padding: 15px; border-radius: 10px;">
        <h3>Selectează o opțiune de mai sus</h3>
    </div>
</div>
"""

# 2. RENDERIZARE
components.html(app_html, height=800)
# ... (Codul tău de sus: CSS, Logo, Header)

# ... (Aici ai deja butoanele tale, lasă-le așa)
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

if c1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if c2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if c3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if c4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.divider()

# --- ADUGĂ ACEASTA PARTE SUB DIVIDER ---
# Logica de conținut (ce apare în chenar)
if st.session_state.activ == 'CHAT':
    st.write("### 💬 Chat Live")
    # Aici poți adăuga chat-ul tău
    if "msgs" not in st.session_state: st.session_state.msgs = []
    text = st.chat_input("Scrie mesaj...")
    if text: st.session_state.msgs.append(text)
    for m in st.session_state.msgs: st.write(f"💬 {m}")

elif st.session_state.activ == 'TRAINS':
    st.write("### 🚂 Status Trenuri")
    st.info("Aici vor apărea informațiile despre trenuri.")

elif st.session_state.activ == 'LCY':
    st.write("### ✈️ LCY Live")
    st.info("Aici vor apărea zborurile LCY.")

elif st.session_state.activ == 'LHR':
    st.write("### ✈️ LHR Live")
    st.info("Aici vor apărea zborurile LHR.")
