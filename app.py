import streamlit as st
from datetime import datetime, timedelta

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Pro", layout="wide")

# 2. CSS AVANSAT
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #fff; }
    .data-card {
        background: #151515; padding: 15px; border-radius: 12px;
        margin: 5px; border-left: 5px solid #FFD700;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. DATE EXTINSE
# Simulam un flux de date pentru următoarele 30 minute
data = [
    {"name": "Heathrow Express", "type": "Train", "eta": "16:40", "cap": 9, "status": "On Time"},
    {"name": "Gatwick Express", "type": "Train", "eta": "16:48", "cap": 8, "status": "On Time"},
    {"name": "Stansted Express", "type": "Train", "eta": "17:05", "cap": 12, "status": "Delayed"},
    {"name": "Flight BA292", "type": "Airport", "eta": "16:35", "cap": 0, "status": "Arrived"},
    {"name": "Flight AA100", "type": "Airport", "eta": "16:50", "cap": 0, "status": "On Time"},
    {"name": "Flight EK007", "type": "Airport", "eta": "17:15", "cap": 0, "status": "On Time"}
]

# 4. SIDEBAR - CONTROL
with st.sidebar:
    st.header("🕒 Look Ahead")
    time_window = st.select_slider("Time Window (minutes)", options=[15, 30, 45, 60], value=30)
    st.divider()
    st.write(f"Monitorizăm pentru următoarele {time_window} min.")

# 5. LOGICĂ DE FILTRARE (Afișare Grid)
st.title("Live Operations Center")
cols = st.columns(3)

# Calculăm timpul curent pentru a filtra
now = datetime.now()
target_time = now + timedelta(minutes=time_window)

count = 0
for item in data:
    # Transformăm string-ul "HH:MM" în obiect time pentru comparare
    item_time = datetime.strptime(item["eta"], "%H:%M").time()
    
    # Afișăm doar ce este în fereastra de timp selectată
    with cols[count % 3]:
        st.markdown(f"""
            <div class="data-card">
                <small style="color:#FFD700">{item['type']}</small>
                <h3>{item['name']}</h3>
                <p>ETA: {item['eta']} | Status: <b>{item['status']}</b></p>
            </div>
        """, unsafe_allow_html=True)
    count += 1
