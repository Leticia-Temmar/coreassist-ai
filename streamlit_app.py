import streamlit as st
import requests

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="CoreAssist AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("CoreAssist AI")
st.sidebar.caption("Gemini 2.0 Flash")

rag_mode = st.sidebar.selectbox(
    "Knowledge source",
    ["PDF documents", "Contacts"]
)

if rag_mode == "PDF documents":
    api_url = "http://127.0.0.1:8000/ask/pdf-rag"
else:
    api_url = "http://127.0.0.1:8000/ask/contacts-rag"

# ---------------------------------------------------
# Sidebar Custom Buttons
# ---------------------------------------------------

st.sidebar.markdown("""
<style>

.sidebar-button {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.2s;
}

.sidebar-button:hover {
    background-color: rgba(120, 120, 120, 0.12);
}

</style>

<div class="sidebar-button">💬 New Chat</div>

<div class="sidebar-button">🔎 Search</div>

""", unsafe_allow_html=True)
# ---------------------------------------------------
# Recent Conversations
# ---------------------------------------------------

st.sidebar.markdown("### Recent Conversations")

st.sidebar.markdown("""
<style>
.recent-item {
    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 4px;
    cursor: pointer;
    font-size: 15px;
}

.recent-item:hover {
    background-color: rgba(120, 120, 120, 0.12);
}
</style>

<div class="recent-item">💬 HR department contacts</div>
<div class="recent-item">💬 IT/IS employees</div>
<div class="recent-item">💬 Sales team information</div>
<div class="recent-item">💬 Company services</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# Example Questions
# ---------------------------------------------------

if len(st.session_state.messages) == 0:
    st.markdown(
        "<div style='"
        "display:flex;"
        "align-items:center;"
        "justify-content:center;"
        "gap:12px;"
        "margin-top:120px;"
        "margin-bottom:-35px;"
        "'>"
        "<span style='font-size:42px;'>🤖</span>"
        "<span style='font-size:22px; font-weight:600;'>"
        "How can I help you today ✨?"
        "</span>"
        "</div>",
        unsafe_allow_html=True
    )



# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------
st.markdown("""
<style>

.stChatInput {
    padding-bottom: 200px;
}

</style>
""", unsafe_allow_html=True)
user_question = st.chat_input(
    "Ask anything about your company knowledge..."
)

# ---------------------------------------------------
# User Question Handling
# ---------------------------------------------------

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    try:
        response = requests.post(
            api_url,
            json={"question": user_question},
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        ai_answer = data.get(
            "answer",
            "No answer returned by the API."
        )

    except requests.exceptions.ConnectionError:
        ai_answer = "❌ Could not connect to FastAPI backend."

    except requests.exceptions.Timeout:
        ai_answer = "⏳ Request timeout. Gemini or backend may be slow."

    except Exception as error:
        ai_answer = f"❌ Error: {error}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_answer
    })

    st.rerun()