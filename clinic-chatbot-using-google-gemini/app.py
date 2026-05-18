import streamlit as st
import time
from chatbot.gemini_client import GeminiClient
from chatbot.memory_manager import MemoryManager
from chatbot.prompt_builder import build_prompt


# ==============================
# Page Config
# ==============================

st.set_page_config(
    page_title="PharmaGen AI",
    page_icon="💊",
    layout="wide"
)

# ==============================
# Custom CSS (🔥 PRO UI)
# ==============================

st.markdown("""
<style>
.chat-title {
    font-size: 32px;
    font-weight: bold;
    color: #2E86C1;
}
.sub-title {
    color: gray;
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 13px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# Header
# ==============================

st.markdown('<div class="chat-title">💊 PharmaGen AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your Intelligent Pharmaceutical Assistant</div>', unsafe_allow_html=True)


# ==============================
# Sidebar (🔥 INDUSTRY FEATURE)
# ==============================

with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Conversation"):
        if "memory" in st.session_state:
            st.session_state.memory.clear_memory()
        st.rerun()

    st.markdown("---")
    st.info("💡 Tip: Ask detailed pharma questions for better results")

    st.markdown("---")
    st.caption("👨‍💻 Built by Mahesh Bodhankar")


# ==============================
# Session State
# ==============================

if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

if "client" not in st.session_state:
    st.session_state.client = GeminiClient()


# ==============================
# Chat Display
# ==============================

for msg in st.session_state.memory.get_history():
    with st.chat_message(msg["role"]):
        st.write(msg["parts"][0])


# ==============================
# Chat Input
# ==============================

user_input = st.chat_input("💬 Ask about medicines, pharma industry, drugs...")

if user_input:
    memory = st.session_state.memory
    client = st.session_state.client

    # Show user message instantly
    with st.chat_message("user"):
        st.write(user_input)

    memory.add_user_message(user_input)

    prompt = build_prompt(user_input)

    # ==============================
    # AI Response with Spinner (🔥 UX)
    # ==============================

    with st.chat_message("assistant"):
        with st.spinner("💡 Thinking..."):
            time.sleep(0.5)  # smooth UX feel
            response = client.generate_response(prompt, memory.get_history())

        st.write(response)

    memory.add_bot_message(response)


# ==============================
# Footer
# ==============================

st.markdown("""
<hr>
<div class="footer">
💊 PharmaGen AI • Production-Ready GenAI System  
🚀 Built with Streamlit + Gemini API  
👨‍💻 Mahesh Bodhankar 
</div>
""", unsafe_allow_html=True)
