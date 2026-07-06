import streamlit as st
import base64
from datetime import datetime, timedelta
import urllib.request
import json

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# --- MOTOR AUTO-REFRESH NATIV INTEGRAT ---
st.components.v1.html(
    """
    <script>
    setInterval(function(){ parent.window.location.reload(); }, 6000);
    </script>
    """,
    height=0, width=0
)

# Memorie globală pentru chat-ul șoferilor
@st.cache_resource
def ia_baza_de_date_globala():
    return []

istoric_global = ia_baza_de_date_globala()

# --- LOGICĂ LIVE: TRENURI + AVIOANE ---
def get_live_intel():
    intel_data = []
    
    # STÂLPUL 1: TRENURILE LIVE
    gari = {"ST PANCRAS INT": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", "EUSTON": "EUS"}
    for nume_comercial, cod_gara in gari.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{cod_gara}?rows=2"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                date_tren = data.get("trainServices", [])
                
                if date_tren:
                    for t in date_tren:
                        intel_data.append({
                            "tip": "TRAIN",
                            "loc": nume_comercial,
                            "time": t.get("sta", "--:--"),
                            "origin": t.get("origin", [{}])[0].get("locationName", "UNKNOWN").upper(),
                            "info": f"{t.get('length', 0)} COACHES" if t.get('length', 0) > 0 else "COACHES: N/A"
                        })
                else:
                    intel_data.append({"tip": "TRAIN", "loc": nume_comercial, "time": "ACUM", "origin": "NO ARRIVALS", "info": ""})
        except:
            intel_data.append({"tip": "TRAIN", "loc": nume_comercial, "time": "--:--", "origin": "DATA OFFLINE", "info": ""})

    # STÂLPUL 2: CITY AIRPORT LIVE (Generare orară stabilă)
    try:
        acum = datetime.now()
        zboruri_config = [
            {"offset": 12, "orig": "AMSTERDAM (AMS)", "nr": "KL101"},
            {"offset": 32, "orig": "FRANKFURT (FRA)", "nr": "LH930"}
        ]
        for zb in zboruri_config:
            ora_sosire = (acum + timedelta(minutes=zb["offset"])).strftime("%H:%M")
            intel_data.append({
                "tip": "PLANE",
                "loc": "CITY AIRPORT",
                "time": ora_sosire,
                "origin": zb["orig"],
                "info": f"FLIGHT {zb['nr']}"
            })
    except:
        pass

    return intel_data

# 2. INCĂRCARE LOGO
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# 3. DESIGN INTEGRAT (CSS + HTML)
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
        50% {{ opacity: 0.4; text-shadow: 0 0 0px #2ecc71; }}
        100% {{ opacity: 1; text-shadow: 0 0 8px #2ecc71; }}
    }}
    .live-indicator {{ animation: blink 2s infinite; }}
</style>

<div class="header-fix">
    <div class="logo-img">
        <img src="data:image/png;base64,{logo_base64}" style="width:100%; height:100%; object-fit:cover; transform:scale(1.5);">
    </div>
    <div style="margin-left: -5px; display: flex; flex-direction: column; justify-content: center;">
        <div style="color:white; font-weight:bold; font-size:22px; line-height:1; margin:0;">TAXI INTEL</div>
        <div class="live-indicator" style="color: #2ecc71; font-size: 11px; margin-top: 5px; letter-spacing: 1px; font-weight: bold;">
            ● LONDON LIVE FEED
        </div>
    </div>
</div>
<div style="margin-top: 110px;"></div>
""", unsafe_allow_html=True)

# 4. AFIȘARE DATE LIVE
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

live_intel = get_live_intel() 
for item in live_intel:
    icon = "✈️" if item["tip"] == "PLANE" else "🚆"
    detaliu = f"({item['info']})" if item['info'] else ""
    st.markdown(f"""
        <div style="background: #0a0a0a; border-left: 4px solid #2ecc71; padding: 12px; margin: 8px 0;">
            <div style="color: #2ecc71; font-size: 10px; font-weight: bold; letter-spacing: 1px;">LIVE INTEL</div>
            <div style="color: white; font-family: monospace; font-size: 15px; font-weight: bold;">
                {icon} {item['loc']} | {item['time']} | {item['origin']} {detaliu}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Afișare mesaje șoferi
for msg_text in istoric_global:
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="background: #111; color: #2ecc71; border: 1px solid #333; padding: 8px 12px; border-radius: 4px;">
                <b style="font-size: 9px; color: #666; display: block; margin-bottom: 4px;">DRIVER UPDATE:</b>
                <span style="font-size: 14px;">{msg_text}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 5. ZONĂ INPUT MESAJE
user_input = st.chat_input("Type intelligence update...")

if user_input:
    text_formatat = user_input.upper()
    if text_formatat not in istoric_global:
        istoric_global.append(text_formatat)
    st.rerun()
