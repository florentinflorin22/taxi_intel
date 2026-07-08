import streamlit as st
import requests

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="wide")

# 2. FUNCȚIE PENTRU DATE LIVE (TfL API)
def get_train_data(station_id):
    # ID-ul pentru Waterloo este: 940GZZLUWLO
    url = f"https://api.tfl.gov.uk/StopPoint/{station_id}/Arrivals"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# 3. INTERFAȚĂ
st.title("Live London Transport Data")

# Selectie statie (folosim ID-uri reale TfL)
stations = {
    "Waterloo": "940GZZLUWLO",
    "Paddington": "940GZZLUPAD",
    "Victoria": "940GZZLUVIC"
}

selected = st.selectbox("Select Station for Live Data:", list(stations.keys()))

if st.button("Fetch Live Data"):
    data = get_train_data(stations[selected])
    
    if data:
        # Sortăm după timpul de sosire
        data.sort(key=lambda x: x['timeToStation'])
        
        for train in data[:5]: # Afișăm primele 5 sosiri
            mins = train['timeToStation'] // 60
            st.success(f"Train to {train['destinationName']} arriving in {mins} minutes.")
    else:
        st.error("Could not fetch live data.")
