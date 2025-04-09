import streamlit as st
from mistralai import Mistral

# Streamlit UI
st.set_page_config(page_title="SmartVoyage - AI Trip Planner", page_icon="🌍")
st.title("🌍 SmartVoyage")
st.subheader("Your personal A.I. travel planner ✈️")

# Mistral API settings
MISTRAL_API_KEY = "zODRqv1jxj9VEdY7o4tuV1gDvWxlGIJj"  # Replace with your real key
client = Mistral(api_key=MISTRAL_API_KEY)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are SmartVoyage, a helpful AI travel planner."}
    ]

# Display previous conversation (excluding system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for user message
user_input = st.chat_input("Tell me where you'd like to go and any preferences...")

# Function to get response from Mistral
def get_trip_plan(chat_history):
    response = client.chat.complete(
        model="mistral-tiny",
        messages=chat_history
    )
    return response.choices[0].message.content

# Handle user input
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare chat history for the API
    chat_history = st.session_state.messages

    # Get assistant's reply
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip... ✨"):
            reply = get_trip_plan(chat_history)
            st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
