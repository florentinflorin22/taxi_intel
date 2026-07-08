import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. CODUL HTML/CSS "PIXEL-PERFECT"
# Aici construim exact layout-ul din schița ta
app_html = """
<div style="background-color: black; color: white; height: 100vh; padding: 20px; font-family: sans-serif;">
    <div style="display: flex; align-items: center; border-bottom: 2px solid #2ecc71; padding-bottom: 10px;">
        <div style="width: 50px; height: 50px; background: #333; border-radius: 50%; margin-right: 15px;"></div>
        <h2 style="margin: 0;">TAXI INTEL</h2>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
        <button onclick="parent.postMessage('CHAT', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">CHAT</button>
        <button onclick="parent.postMessage('TRAINS', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">TRAINS</button>
        <button onclick="parent.postMessage('LCY', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">LCY</button>
        <button onclick="parent.postMessage('LHR', '*')" style="height: 50px; border-radius: 10px; border: 1px solid #2ecc71; background: #111; color: white;">LHR</button>
    </div>
    
    <div id="content" style="margin-top: 30px; border: 1px solid #333; padding: 15px; border-radius: 10px;">
        <h3>Selectează o opțiune de mai sus</h3>
    </div>
</div>
"""

# 2. RENDERIZARE
components.html(app_html, height=800)
