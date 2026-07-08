import streamlit as st
import base64

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# 2. FUNCȚIE LOGO
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# 3. DESIGN CSS (Bloc corect, nu mai da eroare)
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display:none; }

    .header-fix {
        position: fixed; top: 0; left: 0; right: 0;
        background: #000000; padding: 10px 15px; z-index: 1000;
        border-bottom: 1px solid #1a1a1a;
        display: flex; align-items: center; height: 80px;
    }

    .logo-img {
        width: 60px !important; 
        height: 60px !important;
        border-radius: 50%;
        border: 2px solid #2ecc71;
        margin-right: 15px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .logo-img img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    .live-indicator { color: #2ecc71; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 4. HEADER
st.markdown(f"""
<div class="header-fix">
    <div class="logo-img">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    <div>
        <div style="color:white; font-weight:bold; font-size:20px;">TAXI INTEL</div>
        <div class="live-indicator">● LONDON LIVE FEED</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. SPAȚIU ȘI CHAT
st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
    
user_input = st.chat_input("Type a message...")
if user_input:
    st.session_state.messages.append(user_input)
    
for msg in st.session_state.messages:
    st.write(f"💬 {msg}")
