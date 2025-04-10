import streamlit as st
from mistralai import Mistral

# --- Streamlit UI ---
st.set_page_config(page_title="SmartVoyage - AI Trip Planner", page_icon="🌍")

# Inject CSS for chat bubbles
st.markdown("""
    <style>
    .chat-bubble {
        padding: 12px 16px;
        margin: 10px 0;
        border-radius: 20px;
        max-width: 80%;
        display: inline-block;
        font-size: 16px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .user {
        background-color: #DCF8C6;
        color: #000;
        margin-left: auto;
        text-align: right;
    }
    .assistant {
        background-color: #F1F0F0;
        color: #000;
        margin-right: auto;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 SmartVoyage")
st.subheader("Your personal A.I. travel planner ✈️")

# --- Mistral API settings ---
MISTRAL_API_KEY = "zODRqv1jxj9VEdY7o4tuV1gDvWxlGIJj"  # Replace with your real key
client = Mistral(api_key=MISTRAL_API_KEY)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are SmartVoyage, a helpful AI travel planner."}
    ]

# --- Show previous messages (styled like chat bubbles) ---
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f'<div class="chat-bubble user">{content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div class="chat-bubble assistant">{content}</div>', unsafe_allow_html=True)

# --- Chat input ---
user_input = st.chat_input("Tell me where you'd like to go and any preferences...")

# --- Get response from Mistral ---
def get_trip_plan(chat_history):
    response = client.chat.complete(
        model="mistral-tiny",
        messages=chat_history
    )
    return response.choices[0].message.content

# --- Handle user input ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get assistant's reply
    chat_history = st.session_state.messages
    with st.spinner("Planning your trip... ✨"):
        reply = get_trip_plan(chat_history)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()  # To refresh the UI with new messages
