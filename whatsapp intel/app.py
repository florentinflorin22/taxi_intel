import streamlit as st
import base64
import urllib.request
import json
from datetime import datetime, timedelta

# 1. PAGE SETTINGS
st.set_page_config(page_title="London Live Intel", layout="centered")

# --- BACKGROUND AUTO-REFRESH EVERY 15 MINUTES ---
st.components.v1.html(
    """
    <script>
    setInterval(function(){ parent.window.location.reload(); }, 900000);
    </script>
    """,
    height=0, width=0
)

# Global memory
@st.cache_resource
def get_global_database():
    return []

global_history = get_global_database()

# Station color map
STATION_COLORS = {
    "ST PANCRAS INT": "#e74c3c", "PADDINGTON": "#f1c40f", "VICTORIA": "#3498db",
    "EUSTON": "#9b59b6", "KINGS CROSS": "#e67e22", "WATERLOO": "#1abc9c",
    "LONDON BRIDGE": "#f39c12", "LIVERPOOL STREET": "#2ecc71", "CHARING CROSS": "#d35400",
    "CITY AIRPORT": "#3498db"
}

# --- TEXT INPUT (MUTAT SUS PENTRU VITEZĂ) ---
user_input = st.chat_input("Type update...")
if user_input:
    global_history.append(user_input.upper())
    st.rerun()

# --- LIVE LOGIC ---
def get_top_intel():
    all_trains = []
    flights = []
    # (Logica rămâne aceeași, dar se execută abia după ce am procesat input-ul)
    # 1. LCY
    try:
        now = datetime.now()
        flight_config = [
            {"offset": 10, "orig": "AMSTERDAM (AMS)", "nr": "KL101"},
            {"offset": 30, "orig": "FRANKFURT (FRA)", "nr": "LH930"}
        ]
        for fl in flight_config:
            arrival_time = (now + timedelta(minutes=fl["offset"])).strftime("%H:%M")
            flights.append({"type": "PLANE", "station": "CITY AIRPORT", "time": arrival_time, "origin": fl["orig"], "info": f"FLIGHT {fl['nr']}"})
    except: pass

    # 2. TRAINS
    stations = {"ST PANCRAS INT": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", "EUSTON": "EUS", "KINGS CROSS": "KGX", "WATERLOO": "WAT", "LONDON BRIDGE": "LBG", "LIVERPOOL STREET": "LST", "CHARING CROSS": "CHX"}
    for station_name, station_code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{station_code}?rows=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1) as response:
                data = json.loads(response.read().decode())
                trains = data.get("trainServices", [])
                if trains:
                    for t in trains:
                        all_trains.append({"type": "TRAIN", "station": station_name, "time": t.get("sta", "--:--"), "origin": t.get("origin", [{}])[0].get("locationName", "UNKNOWN").upper(), "info": f"{t.get('length', 0)} COACHES"})
        except: pass
    
    all_trains.sort(key=lambda x: x["time"])
    return flights + all_trains[:5]

# --- UI DISPLAY ---
st.markdown("""<style>.stApp { background-color: #000000 !important; } .station-name { font-size: 18px !important; font-weight: 800 !important; text-transform: uppercase; }</style>""", unsafe_allow_html=True)

# Display Chat first (so it's snappy)
for msg in global_history:
    st.markdown(f'<div style="background:#111; color:#2ecc71; padding:8px; margin:5px; border-radius:4px; font-weight:bold;">DRIVER: {msg}</div>', unsafe_allow_html=True)

# Display Intel
for item in get_top_intel():
    color = STATION_COLORS.get(item["station"], "#ffffff")
    st.markdown(f"""
        <div style="background: #0a0a0a; border-left: 4px solid {color}; padding: 10px; margin: 6px 0;">
            <div class="station-name" style="color: {color};">{item['station']}</div>
            <div style="color: white; font-family: monospace; font-size: 14px;">{"✈️" if item["type"]=="PLANE" else "🚆"} {item['time']} | FROM: {item['origin']}</div>
        </div>
    """, unsafe_allow_html=True)
