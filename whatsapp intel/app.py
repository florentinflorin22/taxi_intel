import streamlit as st
import json
import os

# Fișierul unde salvăm mesajele pe server
DB_FILE = "chat_db.json"

def load_db():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

st.set_page_config(page_title="Taxi Intel", layout="centered")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .box { background: #111; padding: 12px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- LOGICĂ ---
st.markdown("<h2 style='text-align: center;'>TAXI INTEL</h2>", unsafe_allow_html=True)

# Secțiune Chat
user_input = st.chat_input("Write a message...")
if user_input:
    db = load_db()
    db.append(user_input.upper())
    save_db(db)
    st.rerun()

# Afișare mesaje (se încarcă de pe server)
db = load_db()
for msg in reversed(db):
    st.markdown(f'<div class="box">{msg}</div>', unsafe_allow_html=True)
