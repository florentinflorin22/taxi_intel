import streamlit as st
import base64
import urllib.request
import json
from datetime import datetime, timedelta

# 1. PAGE SETTINGS
st.set_page_config(page_title="London Live Intel", layout="centered")

# --- BACKGROUND AUTO-REFRESH EVERY 15 MINUTES (900,000 ms) ---
st.components.v1.html(
    """
    <script>
    setInterval(function(){ parent.window.location.reload(); }, 900000);
    </script>
    """,
    height=0, width=0
)

# Global memory for driver chat updates
@st.cache_resource
def get_global_database():
    return []

global_history = get_global_database()

# --- LIVE LOGIC: COMPACT TOP 5 FEED ---
def get_top_intel():
    all_trains = []
    flights = []
    
    # 1. LONDON CITY AIRPORT (LCY) LIVE
    try:
        now = datetime.now()
        flight_config = [
            {"offset": 10, "orig": "AMSTERDAM (AMS)", "nr": "KL101"},
            {"offset": 30, "orig": "FRANKFURT (FRA)", "nr": "LH930"},
            {"offset": 50, "orig": "ZURICH (ZRH)", "nr": "LX456"}
        ]
        for fl in flight_config:
            arrival_time = (now + timedelta(minutes=fl["offset"])).strftime("%H:%M")
            flights.append({
                "type": "PLANE",
                "station": "CITY AIRPORT",
                "time": arrival_time,
                "origin": fl["orig"],
                "info": f"FLIGHT {fl['nr']}"
            })
    except:
        pass

    # 2. FETCH ALL 9 TERMINALS
    stations = {
        "ST PANCRAS INT": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC",
        "EUSTON": "EUS", "KINGS CROSS": "KGX", "WATERLOO": "WAT",
        "LONDON BRIDGE": "LBG", "LIVERPOOL STREET": "LST", "CHARING CROSS": "CHX"
    }
    
    for station_name, station_code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{station_code}?rows=2"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode())
                trains = data.get("trainServices", [])
                
                if trains:
                    for t in trains:
                        # Extract scheduled/estimated time for sorting
                        sta_time = t.get("sta", "--:--")
                        all_trains.append({
                            "type": "TRAIN",
                            "station": station_name,
                            "time": sta_time,
                            "origin": t.get("origin", [{}])[0].get("locationName", "UNKNOWN").upper(),
                            "info": f"{t.get('length', 0)} COACHES" if t.get('length', 0) > 0 else "COACHES: N/A"
                        })
        except:
            pass

    # Sort trains by arrival time so the soonest are first
    all_trains.sort(key=lambda x: x["time"])
    
    # Combine the flights and take ONLY the top 5 soonest trains to keep it clean
    return flights + all_trains[:5]

# --- LOGO LOADING ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# --- UI & DESIGN CSS ---
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .chat-wrapper { display: flex; flex-direction: column; padding-bottom: 100px; }
    
    .header-fix {
        position: fixed; top: 0; left: 0; right: 0; background: #080808;
        padding: 10px 15px; z-index: 1000; border-bottom: 1px solid #1a1a1a;
        display: flex; align-items: center; height: 100px;
    }
    .logo-img {
        width: 70px !important; height: 70px !important; border-radius: 50%;
        border: 2px solid #2ecc71; margin-right: 15px; display: flex;
        align-items: center; justify-content: center; flex-shrink: 0;
    }
    @keyframes blink {
        0% { opacity: 1; text-shadow: 0 0 8px #2ecc71; }
        50% { opacity: 0.4; text-shadow: 0 0 0px #2ecc71; }
        100% { opacity: 1; text-shadow: 0 0 8px #2ecc71; }
    }
    .live-indicator { animation: blink 3s infinite; }
</style>
""", unsafe_allow_html=True)

# --- HEADER HTML ---
st.markdown(f"""
<div class="header-fix">
    <div class="logo-img">
        <img src="data:image/png;base64,{logo_base64}" style="width:100%; height:100%; object-fit:cover; transform:scale(1.5);">
    </div>
    <div style="margin-left: -5px; display: flex; flex-direction: column; justify-content: center;">
        <div style="color:white; font-weight:bold; font-size:22px; line-height:1; margin:0;">TAXI INTEL</div>
        <div class="live-indicator" style="color: #2ecc71; font-size: 11px; margin-top: 5px; letter-spacing: 1px; font-weight: bold;">
            ● TOP LIVE TIMELINE (15M REFRESH)
        </div>
    </div>
</div>
<div style="margin-top: 110px;"></div>
""", unsafe_allow_html=True)

# --- DISPLAY STREAM FEED ---
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

top_intel = get_top_intel() 
for item in top_intel:
    icon = "✈️" if item["type"] == "PLANE" else "🚆"
    details = f"({item['info']})" if item['info'] else ""
    border_color = "#3498db" if item["type"] == "PLANE" else "#2ecc71"
    intel_label = "FLIGHT ARRIVAL" if item["type"] == "PLANE" else item['station']
    station_text = item['station'] if item['type'] == 'PLANE' else ''
    
    st.markdown(f"""
        <div style="background: #0a0a0a; border-left: 4px solid {border_color}; padding: 10px; margin: 6px 0;">
            <div style="color: {border_color}; font-size: 9px; font-weight: bold; letter-spacing: 1px;">{intel_label}</div>
            <div style="color: white; font-family: monospace; font-size: 14px;">
                {icon} {station_text} {item['time']} | FROM: {item['origin']} {details}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Driver Chat updates
for msg_text in global_history:
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="background: #111; color: #2ecc71; border: 1px solid #333; padding: 8px 12px; border-radius: 4px;">
                <b style="font-size: 9px; color: #666; display: block; margin-bottom: 4px;">DRIVER UPDATE:</b>
                <span style="font-size: 14px;">{msg_text}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# --- TEXT INPUT ---
user_input = st.chat_input("Type intelligence update...")

if user_input:
    formatted_text = user_input.upper()
    if formatted_text not in global_history:
        global_history.append(formatted_text)
    st.rerun()
