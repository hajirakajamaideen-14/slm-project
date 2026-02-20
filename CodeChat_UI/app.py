import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DevCode AI",
    page_icon="💻",
    layout="wide"
)

# ---------------- PREMIUM UI DESIGN ----------------
st.markdown("""
<style>

/* ===== Animated Gradient Background ===== */
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a1a2e);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ===== Title Styling ===== */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 25px;
}

/* ===== Glass Chat Bubbles ===== */
.stChatMessage {
    border-radius: 20px;
    padding: 15px;
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.06);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    margin-bottom: 15px;
}

/* ===== Floating Input Box ===== */
section[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 25%;
    width: 50%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(15px);
    padding: 10px;
    border-radius: 20px;
    box-shadow: 0 5px 25px rgba(0, 255, 255, 0.4);
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* ===== Buttons ===== */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    color: black;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00ffcc;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">💻 DevCode AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Professional Code-Only Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-bottom:25px;'>
    <span style='background:rgba(0,255,255,0.15); padding:8px 20px; border-radius:20px;'>
        🚀 Powered by CodeGemma 2B • Instant Code Generation
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- OLLAMA SETTINGS ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "hf.co/ehrrh/codegemma-2b-Q8_0-GGUF:Q8_0"

SYSTEM_PROMPT = """
You are a professional coding assistant.
Respond ONLY with valid executable code.
No explanation.
No text.
Return only pure code.
"""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙ Settings")
    temperature = st.slider("Creativity", 0.0, 1.0, 0.2)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.code(msg["content"], language="python")

# ---------------- INPUT ----------------
prompt = st.chat_input("Ask for coding solution...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.code(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Generating Code..."):
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": SYSTEM_PROMPT + "\nUser: " + prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature
                        }
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json().get("response", "")
                else:
                    result = "print('Error: Unable to connect to Ollama')"

            except Exception:
                result = "print('Connection Error')"

        st.code(result, language="python")

    st.session_state.messages.append({"role": "assistant", "content": result})