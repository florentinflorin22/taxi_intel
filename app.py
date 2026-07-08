import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Taxi Intel Ultra Pro", layout="wide")

# CSS pentru un look "Command Center"
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #151515; border-radius: 10px; padding: 15px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# Mapare stații pentru Huxley API
station_map = {
    "Waterloo": "WAT", "Victoria": "VIC", "Paddington": "PAD", 
    "Kings Cross": "KGX", "Euston": "EUS", "St Pancras": "STP", 
    "London Bridge": "LBG", "Liverpool St": "LST", "Charing Cross": "CHX"
}

st.title("🚀 Taxi Intel: COMMAND CENTER")

with st.sidebar:
    selected_hub = st.selectbox("Select Hub:", list(station_map.keys()))
    refresh = st.button("Refresh Live Data")

# Logica de fetch cu gestionare de erori
def get_data(code):
    try:
        url = f"https://huxley2.azurewebsites.net/departures/{code}?expand=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

data = get_data(station_map[selected_hub])

if data and 'trainServices' in data and data['trainServices']:
    st.success(f"LIVE FEED: {selected_hub}")
    
    # Transformăm datele în DataFrame
    services = data['trainServices']
    df = pd.DataFrame(services)
    
    # Selectăm doar coloane utile
    df_clean = df[['destination', 'std', 'etd', 'platform']].rename(columns={
        'destination': 'Destination', 'std': 'Scheduled', 'etd': 'Estimated', 'platform': 'Plat'
    })
    
    st.table(df_clean)
else:
    st.warning("Live data feed is temporarily unreachable. Switching to simulation mode...")
    # Date simulate de rezervă (pentru a nu lăsa pagina goală)
    sim_data = pd.DataFrame({
        'Destination': ['Heathrow', 'Gatwick', 'Brighton'],
        'Scheduled': ['17:00', '17:15', '17:30'],
        'Estimated': ['17:05', '17:15', '17:35'],
        'Plat': ['12', '4', '8']
    })
    st.table(sim_data)
