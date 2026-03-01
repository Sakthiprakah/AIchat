import streamlit as st

from datetime import datetime
import google.generativeai as genai


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ChatterPufzz",
    page_icon="🤖",
    layout="centered"
)

# ================= SESSION =================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "dark" not in st.session_state:
    st.session_state.dark = True

# ================= SIDEBAR =================
st.sidebar.title("⚙ Settings")
# st.session_state.dark = st.sidebar.checkbox("🌙 Dark Mode", st.session_state.dark)

# ================= THEME =================
if st.session_state.dark:
    BG = "#0f172a"
    USER = "#0d4726ff"
    AI = "#1e293b"
    TXT = "#ffffff"
else:
    BG = "#f8fafc"
    USER = "#111110"
    AI = "#e5e7eb"
    TXT = "#000000"

# ================= CSS =================
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
}}

.chat {{
    max-width: 750px;
    margin: auto;
    padding: 10px;
}}

.user {{
    background: {USER};
    color: white;
    padding: 12px;
    border-radius: 15px;
    margin: 6px 0;
    text-align: right;
}}

.ai {{
    background: {AI};
    color: {TXT};
    padding: 12px;
    border-radius: 15px;
    margin: 6px 0;
    text-align: left;
}}

.time {{
    font-size: 11px;
    opacity: 0.6;
    margin-top: 4px;
}}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🤖 Wellcome Chatter Pufz")
st.caption("what kind of help i do")

# ================= AI LOGIC =================
def ai_engine(text):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return f"⚠ Error: {e}"
# ================= CHAT UI =================
st.markdown("<div class='chat'>", unsafe_allow_html=True)

for msg in st.session_state.chat:
    role = msg["role"]
    st.markdown(
        f"""
        <div class='{role}'>
            {msg['text']}
            <div class='time'>{msg['time']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ================= INPUT =================
msg = st.chat_input("Type your message...")

if msg:
    st.session_state.chat.append({
        "role": "user",
        "text": msg,
        "time": datetime.now().strftime("%H:%M")
    })

    with st.spinner("AI is typing..."):
        reply = ai_engine(msg)

    st.session_state.chat.append({
        "role": "ai",
        "text": reply,
        "time": datetime.now().strftime("%H:%M")
    })

    st.rerun()

# ================= SIDEBAR =================
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat = []
    st.rerun()

if st.sidebar.button("📄 Export Chat"):
    chat_text = ""
    for c in st.session_state.chat:
        chat_text += f"[{c['time']}] {c['role'].upper()}: {c['text']}\n\n"

    st.sidebar.download_button(
        "⬇ Download",
        chat_text,
        file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )