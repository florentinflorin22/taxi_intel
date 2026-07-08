import streamlit as st
import pandas as pd
import requests

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Ultra Pro", layout="wide")

# 2. CSS "COMMAND CENTER"
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: sans-serif; }
    h1, h2, h3 { color: #FFD700 !important; }
    
    table { width: 100% !important; background-color: #0d0d0d !important; border-collapse: collapse !important; }
    th { background-color: #1a1a1a !important; color: #FFD700 !important; text-transform: uppercase; font-size: 0.85em; padding: 12px !important; }
    td { border-bottom: 1px solid #333 !important; padding: 12px !important; }
    tbody tr:nth-child(even) { background-color: #111 !important; }
    
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# 3. CONFIGURARE HUB-URI
station_map = {
    "Waterloo": "WAT", "Victoria": "VIC", "Paddington": "PAD", 
    "Kings Cross": "KGX", "Euston": "EUS", "St Pancras": "STP", 
    "London Bridge": "LBG", "Liverpool St": "LST", "Charing Cross": "CHX"
}

# 4. SIDEBAR
with st.sidebar:
    st.title("⚙️ SYSTEM CONFIG")
    selected_hub = st.selectbox("Select Target Hub:", list(station_map.keys()))
    refresh = st.button("🔄 Refresh Data")

# 5. LOGICĂ API
def get_data(code):
    try:
        url = f"https://huxley2.azurewebsites.net/departures/{code}?expand=true"
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# 6. AFIȘARE
st.title("🚀 Taxi Intel: COMMAND CENTER")
data = get_data(station_map[selected_hub])

if data and 'trainServices' in data and data['trainServices']:
    st.success(f"LIVE FEED ACTIVE: {selected_hub}")
    
    # Procesare date pentru tabel curat
    services = data['trainServices']
    cleaned_data = []
    for s in services:
        dest_list = s.get('destination', [])
        dest_name = dest_list[0]['locationName'] if isinstance(dest_list, list) and dest_list else "Unknown"
        cleaned_data.append({
            'Destination': dest_name,
            'Scheduled': s.get('std'),
            'Estimated': s.get('etd'),
            'Platform': s.get('platform', '-')
        })
    
    st.table(pd.DataFrame(cleaned_data))
else:
    st.warning("Live feed unreachable. Showing simulation mode.")
    st.table(pd.DataFrame({
        'Destination': ['Heathrow', 'Gatwick', 'Stansted'],
        'Scheduled': ['17:00', '17:15', '17:30'],
        'Estimated': ['17:05', '17:15', '17:35'],
        'Platform': ['12', '4', '8']
    }))
