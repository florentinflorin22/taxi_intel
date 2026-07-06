import streamlit as st
import json
import os

# CONFIGURATION AND DESIGN
st.set_page_config(page_title="Taxi Intel", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button { width: 100%; height: 80px; font-weight: bold; background-color: #1a1a1a; 
                            color: #fff; border: 1px solid #333; border-radius: 10px; font-size: 12px; }
    div.stButton > button:hover { background-color: #2ecc71; }
    .box { background: #0a0a0a; padding: 15px; border-radius: 8px; border-left: 4px solid #2ecc71; margin-top: 10px; }
    .stChatInput textarea { background-color: #1a1a1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# DATABASE FOR SYNCHRONIZATION
DB_FILE = "chat_db.json"
def load_db():
    if not os.path.exists(DB_FILE): return []
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return []

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# INITIALIZATION
if 'page' not in st.session_state: st.session_state.page = 'CHAT'

# 2x2 GRID (The 4 squares at the top)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if col1.button("CHAT"): st.session_state.page = 'CHAT'
if col2.button("STATIONS"): st.session_state.page = 'STATIONS'
if col3.button("LCY AIRPORT"): st.session_state.page = 'LCY'
if col4.button("HEATHROW"): st.session_state.page = 'LHR'

st.markdown("---")

# CONTENT LOGIC
if st.session_state.page == 'CHAT':
    st.markdown("### 💬 DRIVER CHAT")
    user_input = st.chat_input("Write a message...")
    if user_input:
        db = load_db()
        db.append(user_input.upper())
        save_db(db)
        st.rerun()
    
    # Display synchronized messages
    for msg in reversed(load_db()):
        st.markdown(f'<div class="box" style="border-left-color:#3498db;">{msg}</div>', unsafe_allow_html=True)

elif st.session_state.page == 'STATIONS':
    st.markdown("### 🚆 TRAIN STATIONS")
    st.markdown('<div class="box">Stations loading...</div>', unsafe_allow_html=True)

elif st.session_state.page == 'LCY':
    st.markdown("### ✈️ CITY AIRPORT")
    st.markdown('<div class="box">Monitoring LCY...</div>', unsafe_allow_html=True)

elif st.session_state.page == 'LHR':
    st.markdown("### ✈️ HEATHROW")
    st.markdown('<div class="box">Monitoring LHR...</div>', unsafe_allow_html=True)
