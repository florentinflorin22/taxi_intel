import streamlit as st
import base64
import urllib.request
import json
from datetime import datetime, timedelta

# 1. PAGE SETTINGS
st.set_page_config(page_title="London Taxi Intel", layout="wide") # Am trecut pe "wide" pentru split screen

# --- AUTO-REFRESH ---
st.components.v1.html("""<script>setInterval(function(){ parent.window.location.reload(); }, 900000);</script>""", height=0, width=0)

# Global memory
@st.cache_resource
def get_global_database(): return []
global_history = get_global_database()

# --- INPUT (SUS) ---
user_input = st.chat_input("Type update...")
if user_input:
    global_history.append(user_input.upper())
    st.rerun()

# --- LOGIC ---
def get_intel():
    all_trains = []
    # (Logica de preluare trenuri)
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", "EUSTON": "EUS", "WATERLOO": "WAT"}
    for name, code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1) as response:
                data = json.loads(response.read().decode())
                trains = data.get("trainServices", [])
                if trains:
                    t = trains[0]
                    all_trains.append({"station": name, "time": t.get("sta", "--:--"), "origin": t.get("origin", [{}])[0].get("locationName", "???").upper()})
        except: pass
    return all_trains

# --- LAYOUT: DOUĂ COLOANE EGALE ---
col1, col2 = st.columns(2)

# STÂNGA: MESAJUL ȘOFERILOR
with col1:
    st.subheader("DRIVER CHAT")
    for msg in global_history:
        st.markdown(f'<div style="background:#111; color:#2ecc71; padding:10px; margin:5px; border-radius:5px; font-weight:bold;">{msg}</div>', unsafe_allow_html=True)

# DREAPTA: TRENURILE
with col2:
    st.subheader("LIVE TRAINS")
    for item in get_intel():
        st.markdown(f"""
            <div style="background: #0a0a0a; border-left: 4px solid #2ecc71; padding: 10px; margin: 6px 0;">
                <div style="color: #2ecc71; font-weight: bold;">{item['station']}</div>
                <div style="color: white;">🚆 {item['time']} | FROM: {item['origin']}</div>
            </div>
        """, unsafe_allow_html=True)

# CSS pentru un aspect curat
st.markdown("""<style>.stApp { background-color: #000000; color: white; }</style>""", unsafe_allow_html=True)
