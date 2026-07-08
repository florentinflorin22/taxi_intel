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
