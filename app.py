# 1. HEADER (Logo și Titlu pe același rând)
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 15px; border-bottom: 2px solid #2ecc71; padding-bottom: 10px;">
    <img src="data:image/png;base64,{logo_base64}" style="width: 50px; height: 50px; border-radius: 50%;">
    <h2 style="margin: 0; color: white;">TAXI INTEL</h2>
</div>
""", unsafe_allow_html=True)

# 2. BUTOANE ÎN GRILĂ (2 pe rând)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

if 'activ' not in st.session_state: st.session_state.activ = 'CHAT'

if col1.button("CHAT", use_container_width=True): st.session_state.activ = 'CHAT'
if col2.button("TRAINS", use_container_width=True): st.session_state.activ = 'TRAINS'
if col3.button("LCY", use_container_width=True): st.session_state.activ = 'LCY'
if col4.button("LHR", use_container_width=True): st.session_state.activ = 'LHR'

st.markdown("<br>", unsafe_allow_html=True) # Spațiu gol sub butoane
