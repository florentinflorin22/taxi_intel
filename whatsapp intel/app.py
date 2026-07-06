import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Taxi Intel", layout="centered")

# CSS pentru card-uri izolate (fiecare item e un box separat)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .card { background: #111; padding: 12px; margin: 6px 0; border-radius: 8px; border-left: 5px solid #444; }
    .card-chat { border-left-color: #3498db; }
    .card-airport { border-left-color: #f1c40f; }
    .card-train { border-left-color: #2ecc71; }
    .title-mini { font-size: 10px; color: #888; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

if 'db' not in st.session_state: st.session_state.db = []

# CHAT SECTION
st.markdown('<div class="title-mini">DRIVER CHAT</div>', unsafe_allow_html=True)
user_input = st.chat_input("Type update...")
if user_input: st.session_state.db.append(user_input.upper())
for msg in st.session_state.db[-2:]:
    st.markdown(f'<div class="card card-chat">{msg}</div>', unsafe_allow_html=True)

# AIRPORTS SECTION
st.markdown('<div class="title-mini">AIRPORTS</div>', unsafe_allow_html=True)
for apt in ["CITY AIRPORT", "HEATHROW"]:
    st.markdown(f'<div class="card card-airport"><b>{apt}</b><br>STATUS: LIVE</div>', unsafe_allow_html=True)

# TRAINS SECTION
st.markdown('<div class="title-mini">TRAIN STATIONS</div>', unsafe_allow_html=True)
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
                <div class="card card-train">
                    <div style="font-weight:bold;">{name}</div>
                    🚆 {t.get("sta")} | {t.get("origin", [{}])[0].get("locationName")}
                </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f'<div class="card card-train"><b>{name}</b><br>OFFLINE</div>', unsafe_allow_html=True)
