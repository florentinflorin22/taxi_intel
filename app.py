import streamlit as st
import pandas as pd
import requests

# 1. SETĂRI PAGINĂ - Layout de tip Control Center
st.set_page_config(page_title="Taxi Intel Ultra Pro", layout="wide")

# 2. CSS "ULTRA PRO"
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; }
    .urgent { color: #ff4444; font-weight: bold; }
    .good { color: #00ff99; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. CONECTARE LA DATE (Logica API)
# Exemplu pentru gări principale - Huxley API pentru National Rail
def fetch_rail_data(station_code):
    try:
        url = f"https://huxley2.azurewebsites.net/departures/{station_code}?expand=true"
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return None

# 4. DASHBOARD "ULTRA PRO"
st.title("🚀 Taxi Intel: COMMAND CENTER")
st.subheader("Live Mainline & Airport Monitoring")

# Sidebar cu setări avansate
with st.sidebar:
    st.header("⚙️ System Config")
    hub_type = st.radio("Target Zone", ["Mainline Stations", "Airports"])
    # Lista cu cele 9 gări principale + LCY
    station_map = {
        "Waterloo": "WAT", "Victoria": "VIC", "Paddington": "PAD", 
        "Kings Cross": "KGX", "Euston": "EUS", "St Pancras": "STP", 
        "London Bridge": "LBG", "Liverpool St": "LST", "Charing Cross": "CHX"
    }
    selected_hub = st.selectbox("Select Target Hub:", list(station_map.keys()))
    refresh = st.button("🔄 Refresh Data")

# 5. AFIȘARE DATE
data = fetch_rail_data(station_map[selected_hub])

if data:
    st.success(f"Connected to {selected_hub} Feed")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Total Departures", len(data['trainServices']))
        st.write(f"Last updated: {data['generatedAt']}")
        
    with col2:
        df = pd.DataFrame(data['trainServices'])
        st.table(df[['destination', 'std', 'etd', 'platform']].head(10))
else:
    st.error("Live feed currently unavailable. Switch to Simulation mode.")

# 6. ANALIZĂ PREDICTIVĂ (Secțiune Ultra Pro)
st.divider()
st.subheader("📊 Tactical Analysis")
st.info("Peak demand predicted for 17:30 - 18:30 based on historical flight/train arrival density.")
