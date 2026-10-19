
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the API key securely
load_dotenv()
API_KEY = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY", "")
)

st.set_page_config(
    page_title="AI Chat Application",
    page_icon="💬",
    layout="centered"
)

st.title("💬 My AI Chat Application")
st.caption("Powered by Python, Streamlit and Gemini")

if not API_KEY:
    st.error("API key not found. Check your .env file.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Chat Settings")

    instructions = st.text_area(
        "Custom instructions",
        value="You are a helpful AI assistant. Explain clearly and simply.",
        help="Tell the AI how it should respond."
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    max_tokens = st.slider(
        "Maximum response tokens",
        min_value=128,
        max_value=2048,
        value=512,
        step=128
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert conversation into Gemini's message format
    history = []

    for message in st.session_state.messages[:-1]:
        role = "user" if message["role"] == "user" else "model"

        history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=message["content"])]
            )
        )

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat = client.chats.create(
                    model="gemini-flash-latest",
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction=instructions,
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )

                response = chat.send_message(prompt)
                answer = response.text

                if not answer:
                    answer = "The AI returned an empty response. Please try again."

            st.markdown(answer)

            # Show token usage when available
            usage = getattr(response, "usage_metadata", None)

            if usage:
                total_tokens = getattr(
                    usage, "total_token_count", None
                )
                if total_tokens is not None:
                    st.caption(
                        f"Tokens used in this response: {total_tokens}"
                    )

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:
        # Remove the user message so it can be retried
        st.session_state.messages.pop()

        error_message = str(error).lower()

        if "api_key" in error_message or "api key" in error_message:
            st.error("API key error. Check your .env file and API key.")
        elif "429" in error_message or "resource_exhausted" in error_message:
            st.error("API usage limit reached. Please wait and try again.")
        elif "404" in error_message or "not found" in error_message:
            st.error(
                "Model unavailable. Check the current Gemini model names "
                "supported by your API key."
            )
        else:
            st.error(
                "Unable to get an AI response. Check your internet "
                "connection and API settings."
            )
            st.caption(f"Technical details: {error}")
