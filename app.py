import streamlit as st
import google.generativeai as genai


# ----------------------------
# Gemini Configuration
# ----------------------------

API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 800
    }
)


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="AskAI | Intelligent AI Assistant",
    page_icon="💬",
    layout="centered"
)


# ----------------------------
# Custom UI Styling
# ----------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    .title {
        text-align:center;
        font-size:48px;
        font-weight:700;
        margin-bottom:0px;
    }


    .tagline {
        text-align:center;
        font-size:18px;
        opacity:0.7;
        margin-bottom:30px;
    }


    .welcome-card {

        padding:22px;

        border-radius:18px;

        background: rgba(128,128,128,0.08);

        border:1px solid rgba(128,128,128,0.25);

        margin-bottom:25px;

    }


    .feature {

        padding:8px 0px;

        font-size:16px;

    }


    .stChatMessage {

        border-radius:15px;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Header
# ----------------------------

st.markdown(
    """
    <div class="title">
    AskAI ✨
    </div>

    <div class="tagline">
    Your intelligent AI assistant for questions, learning, and creativity.
    </div>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Memory
# ----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



# ----------------------------
# Welcome Screen
# ----------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-card">

        👋 <b>Welcome to AskAI</b>

        <br><br>

        Start a conversation:

        <div class="feature">💻 Explain coding concepts</div>
        <div class="feature">📚 Learn new topics</div>
        <div class="feature">✍️ Write and improve content</div>
        <div class="feature">💡 Ask any question</div>

        </div>
        """,
        unsafe_allow_html=True
    )



# ----------------------------
# Clear Chat Button
# ----------------------------

if len(st.session_state.messages) > 0:

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()



# ----------------------------
# Chat History
# ----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])



# ----------------------------
# User Input
# ----------------------------

question = st.chat_input(
    "Ask anything..."
)



if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)



    # ----------------------------
    # AI Response
    # ----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                prompt = f"""
You are AskAI, a helpful AI assistant.

Your goal is to give clear, simple, human-like answers.

Response style:
- Start with the direct answer.
- Keep normal answers concise.
- Use bullet points for important points.
- Avoid unnecessary long paragraphs.
- Avoid robotic phrases.
- Explain difficult concepts simply.
- Give examples when useful.
- Give detailed answers only when requested.

Answer format:
- Short explanation first.
- Key points if needed.
- Example if useful.

User question:
{question}
"""


                response = model.generate_content(prompt)

                answer = response.text

                st.markdown(answer)


            except Exception:

                answer = (
                    "Sorry, I couldn't generate a response right now. "
                    "Please try again."
                )

                st.markdown(answer)



    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
