import streamlit as st
import urllib.request
import json
from datetime import datetime

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="wide")

# CSS for Split Screen (Table force)
st.markdown("""
<style>
    .main > div { padding-top: 10px; }
    .split-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .split-table td { vertical-align: top; padding: 5px; width: 50%; }
    .chat-box { background: #1a1a1a; padding: 8px; border-radius: 5px; border-left: 3px solid #3498db; margin-bottom: 5px; font-size: 13px; }
    .train-box { background: #0a0a0a; padding: 8px; border-radius: 5px; border-left: 3px solid #2ecc71; margin-bottom: 5px; font-size: 12px; }
    .header-label { color: #888; font-size: 10px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# Data storage
@st.cache_resource
def get_db(): return []
db = get_db()

# Input
user_input = st.chat_input("Update...")
if user_input:
    db.append(user_input.upper())
    st.rerun()

# Logic Trains
def get_trains():
    data_list = []
    stations = {"ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC"}
    for name, code in stations.items():
        try:
            url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
            with urllib.request.urlopen(url, timeout=1) as res:
                t = json.loads(res.read().decode()).get("trainServices", [])[0]
                data_list.append(f'<div class="train-box"><div style="color:#2ecc71">{name}</div>🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}</div>')
        except: continue
    return "".join(data_list)

# Render HTML Table (THE FIX)
st.markdown(f"""
<table class="split-table">
    <tr>
        <td class="header-label">DRIVER CHAT</td>
        <td class="header-label">LIVE TRAINS</td>
    </tr>
    <tr>
        <td>{''.join([f'<div class="chat-box">{m}</div>' for m in db])}</td>
        <td>{get_trains()}</td>
    </tr>
</table>
""", unsafe_allow_html=True)
