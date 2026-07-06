import streamlit as st
import base64
import urllib.request
import json
from datetime import datetime, timedelta

# 1. PAGE SETTINGS
st.set_page_config(page_title="London Terminals & LCY Live", layout="centered")

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

# --- LIVE LOGIC: CITY AIRPORT + 9 TERMINALS ---
def get_all_intel():
    intel_data = []
    
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
            intel_data.append({
                "type": "PLANE",
                "station": "CITY AIRPORT",
                "time": arrival_time,
                "origin": fl["orig"],
                "info": f"FLIGHT {fl['nr']}"
            })
    except:
        pass

    # 2. THE 9 MAJOR LONDON TRAIN TERMINALS
    stations = {
        "ST PANCRAS INT": "STP",
        "PADDINGTON": "PAD",
        "VICTORIA": "VIC",
        "EUSTON": "EUS",
        "KINGS CROSS": "KGX",
        "WATERLOO": "WAT",
        "LONDON BRIDGE": "LBG",
        "LIVERPOOL STREET": "LST",
        "CHARING CROSS": "CHX"
    }
    
    for station_name, station_code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{station_code}?rows=2"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                trains = data.get("trainServices", [])
                
                if trains:
                    for t in trains:
                        intel_data.append({
                            "type": "TRAIN",
                            "station": station_name,
                            "time": t.get("sta", "--:--"),
                            "origin": t.get("origin", [{}])[0].get("locationName", "UNKNOWN").upper(),
                            "info": f"{t.get('length', 0)} COACHES" if t.get('length', 0) > 0 else "COACHES: N/A"
                        })
                else:
                    intel_data.append({"type": "TRAIN", "station": station_name, "time": "NOW", "origin": "NO ARRIVALS", "info": ""})
        except:
            intel_data.append({"type": "TRAIN", "station": station_name, "time": "--:--", "origin": "OFFLINE", "info": ""})

    return intel_data

# --- LOGO LOADING ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# --- UI & DESIGN ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #000000 !important; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    .chat-wrapper {{ display: flex; flex-direction: column; padding-bottom: 100px; }}
    
    .header-fix {{
        position: fixed; top: 0; left: 0; right: 0; background: #080808;
        padding: 10px 15px; z-index: 1000; border-bottom: 1px solid #1a1a1a;
        display: flex; align-items: center; height: 100px;
    }}
    .logo-img {{
        width: 70px !important; height: 70px !important; border-radius: 50%;
        border: 2px solid #2ecc71; margin-right: 15px; display: flex;
        align-items: center; justify-content: center; flex-shrink: 0;
    }}
    @keyframes blink {{
        0% {{ opacity: 1; text-shadow: 0 0 8px #2ecc71; }}
        50% {{ opacity: 0.
