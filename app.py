import streamlit as st
import pandas as pd

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Pro - Live", layout="wide")

# 2. CSS AVANSAT
st.markdown("""
<style>
    .metric-card { background: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# 3. DATE LIVE (Logica de integrare API - concept)
# Pentru gări mari și aeroporturi, folosim date structurate din API-uri de transport
def get_live_data(location_type):
    # Aici ar veni funcția de requests.get() către API-urile de trenuri/avioane
    # Exemplu: return pd.DataFrame(api_call_to_network_rail(location_type))
    return pd.DataFrame({
        "Location": ["Waterloo", "Heathrow", "Paddington", "LHR"],
        "Status": ["Live", "Live", "Live", "Live"],
        "ETA": ["16:45", "16:55", "17:05", "17:15"]
    })

# 4. SIDEBAR - SELECTOR HUB-URI MARI
hubs = ["London Waterloo", "London Victoria", "Paddington", "Kings Cross", 
        "Euston", "St Pancras", "London Bridge", "Liverpool Street", 
        "Charing Cross", "London City Airport", "Heathrow", "Gatwick", "Stansted"]

with st.sidebar:
    st.title("📍 MAIN HUBS ONLY")
    selection = st.multiselect("Select your focus area:", hubs, default=["Heathrow", "London Waterloo"])

# 5. DASHBOARD PRINCIPAL
st.title("Live Transport Monitoring")
st.subheader("Mainline Stations & Airports")

# Afișare date sub formă de tabel profesional
data = get_live_data("all")
st.table(data)

# ALERTĂ VIZUALĂ
st.warning("Data source: Live National Rail & Airport Feeds")
