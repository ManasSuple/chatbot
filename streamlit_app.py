import streamlit as st
from openai import OpenAI

# ---------------- PAGE ----------------
st.set_page_config(page_title="Chatbot")
st.title("💬 Chatbot")

# ---------------- API KEY MANAGEMENT ----------------
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Ask for key only if not stored
if not st.session_state.api_key:
    key_input = st.text_input("OpenAI API Key", type="password")

    if key_input:
        st.session_state.api_key = key_input
        st.rerun()

    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

# Button to change key later
if st.button("Change API Key"):
    st.session_state.api_key = None
    st.rerun()

# Create OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("What is up?"):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        response = st.write_stream(stream)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
