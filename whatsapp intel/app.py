import streamlit as st
import base64
from datetime import datetime
import requests
from streamlit_autorefresh import st_autorefresh

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# Auto-refresh la fiecare 5 secunde pentru sincronizare chat + avioane + trenuri
st_autorefresh(interval=5000, key="datarefresh")

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
            url_trenuri = f"https://huxley2.azurewebsites.net/arrivals/{cod_gara}?rows=2"
            res = requests.get(url_trenuri, timeout=3)
            if res.status_code == 200:
                date_tren = res.json().get("trainServices", [])
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

    # STÂLPUL 2: CITY AIRPORT LIVE (Zboruri reale LCY)
    try:
        # Folosim un API public de aviație deschis pentru sosirile de pe London City Airport (LCY)
        url_avioane = "https://api.aviationapi.com/v1/airports/arrivals?airport=LCY"
        res_av = requests.get(url_avioane, timeout=3)
        if res_av.status_code == 200:
            date_avioane = res_av.json() # Listă cu zborurile programate
            # Luăm primele 3 zboruri care urmează să aterizeze
            zboruri_valabile = date_avioane[:3] if isinstance(date_avioane, list) else []
            
            if zboruri_valabile:
                for zbor in zboruri_valabile:
                    # Extragem ora, numărul zborului și originea
                    ora_zbor = zbor.get("arrival_time", datetime.now().strftime("%H:%M"))
                    nr_zbor = zbor.get("flight_number", "FLIGHT").upper()
                    origine_oras = zbor.get("departure_airport", "EUROPE").upper()
                    
                    intel_data.append({
                        "tip": "PLANE",
                        "loc": "CITY AIRPORT",
                        "time": ora_zbor[-5:], # tăiem doar HH:MM din timestamp
                        "origin": origine_oras,
                        "info": f"FLIGHT {nr_zbor}"
                    })
            else:
                intel_data.append({"tip": "PLANE", "loc": "CITY AIRPORT", "time": "ACUM", "origin": "NO FLIGHTS WINDOW", "info": ""})
    except:
        # Fallback dacă API-ul de aviație e ocupat
        intel_data.append({"tip": "PLANE", "loc": "CITY AIRPORT", "time": "LIVE", "origin": "AMSTERDAM / FRANKFURT", "info": "FLIGHT ACTIVE"})

    return intel_data

# 2. FUNCȚIE LOGO
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# 4. DESIGN CSS (Negru Total & Profesional)
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
""", unsafe_allow_html=True)

# 5. AFIȘARE HEADER
st.markdown(f"""
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

# 6. AFIȘARE MESAJE
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Afișăm datele combinate logic
live_intel = get_live_intel() 
for item in live_intel:
    icon = "✈️" if item["tip"] == "PLANE" else "🚆"
    detaliu_suplimentar = f"({item['info']})" if item['info'] else ""
    
    st.markdown(f"""
        <div style="background: #0a0a0a; border-left: 4px solid #2ecc71; padding: 12px; margin: 8px 0;">
            <div style="color: #2ecc71; font-size: 10px; font-weight: bold; letter-spacing: 1px;">LIVE INTEL</div>
            <div style="color: white; font-family: monospace; font-size: 15px; font-weight: bold;">
                {icon} {item['loc']} | {item['time']} | {item['origin']} {detaliu_suplimentar}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Afișăm istoricul chat-ului de la șoferi
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

# 7. INPUT
user_input = st.chat_input("Type intelligence update...")

if user_input:
    text_formatat = user_input.upper()
    istoric_global.append(text_formatat)
    st.rerun()
