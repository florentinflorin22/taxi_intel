import streamlit as st

# 1. SETĂRI PAGINĂ (Fără layout complicat pentru a evita randările lente)
st.set_page_config(page_title="Taxi Intel", layout="centered")

# 2. CSS MINIMALIST (Viteză maximă)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    section[data-testid="stSidebar"] { background-color: #111; }
    .train-card { background:#151515; padding:10px; border-radius:8px; border-left: 5px solid #f1c40f; margin-bottom:8px; }
    .stButton > button { width: 100%; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZARE STARE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'
if 'msgs' not in st.session_state: st.session_state.msgs = []

# 4. SIDEBAR - Butoanele stau aici pentru viteză de navigare
with st.sidebar:
    st.title("TAXI INTEL")
    if st.button("CHAT"): st.session_state.activ = 'CHAT'
    if st.button("TRAINS"): st.session_state.activ = 'TRAINS'
    if st.button("LCY"): st.session_state.activ = 'LCY'
    if st.button("LHR"): st.session_state.activ = 'LHR'

# 5. CONȚINUT - Fără st.rerun() pentru a elimina "gândirea" lentă
if st.session_state.activ == 'CHAT':
    st.subheader("💬 Chat")
    for m in st.session_state.msgs:
        st.write(f"💬 {m}")
    
    text = st.chat_input("Scrie mesaj...")
    if text:
        st.session_state.msgs.append(text)
        # Am eliminat st.rerun() pentru a evita reîncărcarea lentă

elif st.session_state.activ == 'TRAINS':
    st.subheader("🚂 Trenuri Express (8+ Vagoane)")
    # Datele sunt afișate direct, fără procesări complexe în timp real pe mobil
    trenuri = [
        {"nume": "Heathrow Express", "vagoane": 8, "status": "On Time"},
        {"nume": "Gatwick Express", "vagoane": 10, "status": "On Time"}
    ]
    for t in trenuri:
        if t['vagoane'] >= 8:
            st.markdown(f'''<div class="train-card">
                <strong>{t["nume"]}</strong><br>
                Vagoane: {t["vagoane"]} | Status: {t["status"]}
                </div>''', unsafe_allow_html=True)

elif st.session_state.activ == 'LCY':
    st.subheader("✈️ LCY Airport")
    st.write("Monitorizare activă.")

elif st.session_state.activ == 'LHR':
    st.subheader("✈️ LHR Airport")
    st.write("Monitorizare activă.")
