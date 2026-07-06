import streamlit as st
import base64
import urllib.request
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="London Taxi Intel", layout="centered")

# --- AUTO-REFRESH ---
st.components.v1.html("""<script>setInterval(function(){ parent.window.location.reload(); }, 900000);</script>""", height=0, width=0)

@st.cache_resource
def get_global_database(): return []
global_history = get_global_database()

# --- CSS OPTIMIZAT PENTRU MOBIL ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .chat-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border-left: 4px solid #3498db; margin-bottom: 10px; }
    .train-box { background: #0a0a0a; padding: 10px; border-radius: 8px; border-left: 4px solid #2ecc71; margin-bottom: 8px; }
    .header-text { color: #888; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# --- INPUT ---
user_input = st.chat_input("Type update...")
if user_input:
    global_history.append(user_input.upper())
    st.rerun()

# --- AFIȘARE (VERTICAL, DAR CLAR DELIMITAT) ---
st.markdown('<div class="header-text">DRIVER CHAT</div>', unsafe_allow_html=True)
for msg in global_history:
    st.markdown(f'<div class="chat-box">{msg}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-text" style="margin-top:20px;">LIVE TRAINS</div>', unsafe_allow_html=True)

# Logica trenuri (simplificată pentru viteză)
stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", "EUSTON": "EUS", "WATERLOO": "WAT"}
for name, code in stations.items():
    try:
        url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=1) as response:
            data = json.loads(response.read().decode())
            t = data.get("trainServices", [])[0]
            st.markdown(f"""
                <div class="train-box">
                    <div style="color:#2ecc71; font-weight:bold;">{name}</div>
                    <div style="font-family:monospace;">🚆 {t.get('sta')} | FROM: {t.get('origin', [{}])[0].get('locationName', '???')}</div>
                </div>
            """, unsafe_allow_html=True)
    except: pass
