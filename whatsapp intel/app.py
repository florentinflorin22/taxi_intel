import streamlit as st
import urllib.request
import json

# PAGE SETTINGS
st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS - CLEAN AND COMPACT
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: #f39c12; font-size: 12px; font-weight: bold; margin: 15px 0 5px 0; text-transform: uppercase; border-bottom: 1px solid #333; }
    .item-box { background: #0a0a0a; padding: 10px; margin-bottom: 5px; border-radius: 5px; border-left: 4px solid #2ecc71; }
    .chat-box { background: #1a1a1a; padding: 8px; margin-bottom: 5px; border-radius: 5px; border-left: 4px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# Memory
if 'db' not in st.session_state: st.session_state.db = []

# 1. CHAT SECTION
st.markdown('<div class="section-title">DRIVER CHAT</div>', unsafe_allow_html=True)
user_input = st.chat_input("Type update...")
if user_input: st.session_state.db.append(user_input.upper())
for msg in st.session_state.db[-3:]: # Shows last 3 messages
    st.markdown(f'<div class="chat-box">{msg}</div>', unsafe_allow_html=True)

# 2. AIRPORTS SECTION
st.markdown('<div class="section-title">AIRPORTS</div>', unsafe_allow_html=True)
airports = ["CITY AIRPORT", "HEATHROW"]
for apt in airports:
    st.markdown(f'<div class="item-box" style="border-left-color:#3498db;"><b>{apt}</b><br>STATUS: MONITORING...</div>', unsafe_allow_html=True)

# 3. STATIONS SECTION
st.markdown('<div class="section-title">TRAIN STATIONS</div>', unsafe_allow_html=True)
stations = {
    "ST PANCRAS": "STP", "PADDINGTON": "PAD", "VICTORIA": "VIC", 
    "EUSTON": "EUS", "KINGS CROSS": "KGX", "WATERLOO": "WAT", 
    "LONDON BRIDGE": "LBG", "LIVERPOOL ST": "LST", "CHARING CROSS": "CHX"
}

for name, code in stations.items():
    try:
        url = f"https://huxley2.azurewebsites.net/arrivals/{code}?rows=1"
        with urllib.request.urlopen(url, timeout=1) as res:
            t = json.loads(res.read().decode()).get("trainServices", [])[0]
            st.markdown(f"""
                <div class="item-box">
                    <div style="font-weight:bold; color:#2ecc71;">{name}</div>
                    🚆 {t.get("sta")} | FROM: {t.get("origin", [{}])[0].get("locationName")}
                </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f'<div class="item-box" style="border-left-color:#7f8c8d;"><b>{name}</b><br>OFFLINE</div>', unsafe_allow_html=True)
