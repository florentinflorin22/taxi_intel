import streamlit as st

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel", layout="centered")

# 2. CSS PROFESIONAL
st.markdown("""
<style>
    :root {
        --bg-color: #000000;
        --sidebar-bg: #111111;
        --accent-yellow: #FFD700;
        --text-white: #FFFFFF;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-white); }
    section[data-testid="stSidebar"] { background-color: var(--sidebar-bg); }
    .data-card {
        background: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--accent-yellow);
        margin-bottom: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .status-badge { font-weight: bold; color: #2ecc71; float: right; }
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZARE STARE
if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'
if 'msgs' not in st.session_state: st.session_state.msgs = []

# 4. DATE (Simulate - pot fi înlocuite cu API-uri)
transport_data = {
    "TRAINS": [
        {"name": "Heathrow Express", "capacity": 8, "status": "On Time"},
        {"name": "Gatwick Express", "capacity": 10, "status": "On Time"},
        {"name": "Stansted Express", "capacity": 8, "status": "Delayed"}
    ],
    "AIRPORTS": [
        {"name": "London City (LCY)", "arrivals": "Heavy", "delay": "None"},
        {"name": "Heathrow (LHR)", "arrivals": "Moderate", "delay": "15 min"}
    ]
}

# 5. SIDEBAR
with st.sidebar:
    st.title("TAXI INTEL")
    if st.button("CHAT"): st.session_state.activ = 'CHAT'
    if st.button("TRAINS"): st.session_state.activ = 'TRAINS'
    if st.button("LCY"): st.session_state.activ = 'LCY'
    if st.button("LHR"): st.session_state.activ = 'LHR'

# 6. LOGICĂ AFIȘARE
if st.session_state.activ == 'CHAT':
    st.subheader("💬 Chat")
    for m in st.session_state.msgs:
        st.write(f"💬 {m}")
    text = st.chat_input("Scrie mesaj...")
    if text:
        st.session_state.msgs.append(text)

elif st.session_state.activ == 'TRAINS':
    st.subheader("🚂 Express Trains (8+ Carriages)")
    for train in transport_data["TRAINS"]:
        if train["capacity"] >= 8:
            st.markdown(f"""
                <div class="data-card">
                    <strong>{train["name"]}</strong>
                    <span class="status-badge">{train["status"]}</span>
                    <br><small>Capacity: {train["capacity"]} carriages</small>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.activ in ['LCY', 'LHR']:
    st.subheader(f"✈️ {st.session_state.activ} Live Status")
    for airport in transport_data["AIRPORTS"]:
        if st.session_state.activ in airport["name"]:
            st.markdown(f"""
                <div class="data-card">
                    <strong>{airport["name"]}</strong>
                    <br>Arrivals Intensity: {airport["arrivals"]}
                    <br>Current Delay: {airport["delay"]}
                </div>
            """, unsafe_allow_html=True)
