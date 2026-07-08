st.markdown("""
<style>
    :root {
        --bg-color: #000000;
        --sidebar-bg: #111111;
        --accent-yellow: #FFD700;
        --text-white: #FFFFFF;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-white); }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: var(--sidebar-bg); }
    
    /* Card Component */
    .data-card {
        background: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--accent-yellow);
        margin-bottom: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    
    .status-badge {
        font-weight: bold;
        color: #2ecc71;
        float: right;
    }
</style>
""", unsafe_allow_html=True)
