import streamlit as st
import google.generativeai as genai


# ----------------------------
# Gemini Configuration
# ----------------------------

API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="AskAI | Intelligent AI Chat Assistant",
    page_icon="💬",
    layout="centered"
)


# ----------------------------
# Custom Styling
# ----------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f8f9fa;
    }


    h1 {
        text-align: center;
        font-size: 42px;
    }


    .subtitle {
        text-align: center;
        color: #555;
        font-size: 18px;
        margin-bottom: 25px;
    }


    .welcome-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.header("AskAI")

    st.write(
        """
        Your simple AI assistant for:

        • Coding
        • Learning
        • Writing
        • General Questions
        • Problem Solving
        """
    )


    st.divider()


    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.rerun()



# ----------------------------
# Header
# ----------------------------

st.title("AskAI")


st.markdown(
    """
    <div class="subtitle">
    Ask anything. Get clear, natural, and intelligent answers.
    </div>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Chat Memory
# ----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



# ----------------------------
# Welcome Message
# ----------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-box">

        👋 Welcome to AskAI!

        You can ask me about:

        - Programming and technology
        - Science and mathematics
        - Writing and communication
        - General knowledge
        - Everyday questions

        I will provide clear and natural answers.

        </div>
        """,
        unsafe_allow_html=True
    )



# ----------------------------
# Display Chat History
# ----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])



# ----------------------------
# User Input
# ----------------------------

question = st.chat_input(
    "Ask me anything..."
)



if question:


    # Store user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    # Generate AI Response

    with st.chat_message("assistant"):


        with st.spinner("Thinking..."):


            try:

                prompt = f"""
You are AskAI, a smart conversational AI assistant.

Your goal:
Provide natural, human-like answers.

Rules:
- Answer directly first.
- Keep simple questions short.
- Give detailed explanations only when required.
- Do not use phrases like "That's a fantastic question".
- Do not sound robotic or like a textbook.
- Avoid unnecessary headings.
- Use a friendly conversational tone.
- Explain technical concepts clearly with examples.
- Adapt your response style based on the user's question.

User question:
{question}
"""


                response = model.generate_content(prompt)


                answer = response.text


                st.write(answer)



            except Exception as e:

                answer = (
                    "Sorry, I could not generate a response right now. "
                    "Please try again."
                )

                st.write(answer)



    # Store AI response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
