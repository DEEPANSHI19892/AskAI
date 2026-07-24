
import streamlit as st
import google.generativeai as genai


# Gemini Setup
API_KEY = "YOUR_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# Page Configuration
st.set_page_config(
    page_title="AskAI | Intelligent AI Chat Assistant",
    page_icon="💬"
)


# Header
st.title("AskAI")

st.write(
    "Ask anything. Get clear, natural, and intelligent answers."
)


# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User Input
question = st.chat_input(
    "Ask me anything..."
)


if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):
        st.write(question)


    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            prompt = f"""
You are AskAI, a helpful AI assistant.

Rules:
- Answer naturally.
- Avoid robotic language.
- Explain clearly.
- Be friendly and conversational.
- Adjust answer length based on the question.

User question:
{question}
"""


            response = model.generate_content(prompt)

            answer = response.text

            st.write(answer)


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# Clear button

if st.button("Clear Conversation"):

    st.session_state.messages = []

    st.rerun()
