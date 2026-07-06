import streamlit as st
import base64
from datetime import datetime
import time

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# Memorie globală la nivel de server (partajată între laptop și telefon)
@st.cache_resource
def ia_baza_de_date_globala():
    return []

istoric_global = ia_baza_de_date_globala()

def get_live_intel():
    intel_data = [
        {"loc": "ST PANCRAS INT", "time": "15:10", "origin": "PARIS", "coaches": 18},
        {"loc": "PADDINGTON", "time": "15:22", "origin": "BRISTOL", "coaches": 9},
        {"loc": "VICTORIA", "time": "15:25", "origin": "GATWICK EXP", "coaches": 12},
        {"loc": "CITY AIRPORT", "time": "15:30", "origin": "AMSTERDAM", "coaches": 0},
        {"loc": "EUSTON", "time": "15:35", "origin": "MANCHESTER", "coaches": 11}
    ]
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


# --- NOU: Zona auto-refresh pentru mesaje în timp real ---
@st.fragment(run_every=3) # Verifică și actualizează ecranul automat la fiecare 3 secunde
def afiseaza_live_feed():
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    # Afișăm sosirile fixe
    live_arrivals = get_live_intel() 
    for train in live_arrivals:
        icon = "✈️" if "AIRPORT" in train['loc'] else "🚆"
        detail = f"({train['coaches']} COACHES)" if train['coaches'] > 0 else "ARRIVING"
        st.markdown(f"""
            <div style="background: #0a0a0a; border-left: 4px solid #2ecc71; padding: 12px; margin: 8px 0;">
                <div style="color: #2ecc71; font-size: 10px; font-weight: bold; letter-spacing: 1px;">LIVE INTEL</div>
                <div style="color: white; font-family: monospace; font-size: 15px; font-weight: bold;">
                    {icon} {train['loc']} | {train['time']} | {train['origin']} {detail}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Afișăm mesajele din memoria globală
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

# Rulăm zona de afișare
afiseaza_live_feed()


# 7. INPUT
user_input = st.chat_input("Type intelligence update...")

if user_input:
    text_formatat = user_input.upper()
    istoric_global.append(text_formatat)
    st.rerun()