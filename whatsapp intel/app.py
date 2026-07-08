import streamlit as st
import base64

# 1. SETĂRI PAGINĂ
st.set_page_config(page_title="Taxi Intel Live", layout="centered")

# 2. FUNCȚIE LOGO (Asigură-te că ai fișierul logo.png în același folder)
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# 3. ISTORIC MESAJE
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "SYSTEM: Live Feed Active (15m window)"},
        {"role": "bot", "content": "Welcome to Taxi Intel. Standing by for London live updates."},
    ]

# 4. DESIGN CSS (Negru Total & Profesional)
st.markdown(f"""
<style>
    /* Fundalul paginii */
    .stApp {{
        background-color: #000000 !important;
    }}

    /* Ascundem elementele inutile de la Streamlit */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* Containerul de Chat */
    .chat-wrapper {{
        display: flex;
        flex-direction: column;
        padding-bottom: 100px;
    }}

    /* Bule de Chat */
    .bubble {{
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 85%;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        line-height: 1.4;
    }}

    .bot {{
        background-color: #1a1a1a;
        color: #ffffff;
        border-left: 4px solid #2ecc71;
        align-self: flex-start;
    }}

    .user {{
        background-color: #056162;
        color: #ffffff;
        align-self: flex-end;
        border-bottom-right-radius: 4px;
    }}

    .system {{
        color: #2ecc71;
        text-align: center;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
        margin: 15px 0;
        letter-spacing: 1px;
    }}

    .header-fix {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #080808;
        padding: 10px 15px;
        z-index: 1000;
        border-bottom: 1px solid #1a1a1a;
        display: flex;
        align-items: center;
        height: 100px; /* Am mărit de la 85 la 100 ca să aibă loc logo-ul */
    }}

    .logo-img {{
        width: 70px !important; 
        height: 70px !important;
        border-radius: 50%;
        border: 2px solid #2ecc71;
        margin-right: 15px;
        /* Am scos overflow: hidden ca să nu mai taie poza */
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
/* Definim animația de licărire */
    @keyframes blink {{
        0% {{ opacity: 1; text-shadow: 0 0 8px #2ecc71; }}
        50% {{ opacity: 0.4; text-shadow: 0 0 0px #2ecc71; }}
        100% {{ opacity: 1; text-shadow: 0 0 8px #2ecc71; }}
    }}

    .live-indicator {{
        animation: blink 2s infinite; /* Licărește la fiecare 2 secunde */
    }}
</style>
""", unsafe_allow_html=True)

# 5. AFIȘARE HEADER
st.markdown(f"""
<div class="header-fix">
<div class="logo-img">
<img src="data:image/png;base64,{logo_base64}" style="width:100%; height:100%; object-fit:cover; transform:scale(1.5);">
</div>
<div style="margin-left: -5px; display: flex; flex-direction: column; justify-content: center;">
<div style="color:white; font-weight:bold; font-size:22px; line-height:1; margin:0;">
                TAXI INTEL
</div>
<div class="live-indicator" style="
                color: #2ecc71; 
                font-size: 11px; 
                margin-top: 5px; 
                letter-spacing: 1px;
                font-weight: bold;
            ">
                ● LONDON LIVE FEED
</div>
</div>
</div>
<div style="margin-top: 110px;"></div>
""", unsafe_allow_html=True)

# 6. AFIȘARE MESAJE
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        st.markdown(f'<div class="system">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "bot":
        st.markdown(f'<div class="bubble bot">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble user">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 7. INPUT (Tastatura Streamlit, acum stilizată prin CSS-ul nativ)
user_input = st.chat_input("Type a message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Aici poți adăuga un mic bot care răspunde automat
    if "hello" in user_input.lower():
        st.session_state.messages.append({"role": "bot", "content": "Hello driver! How can I help you today?"})
    st.rerun()
