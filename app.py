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

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 850px;
    }


    h1 {
        text-align: center;
        font-size: 42px;
        margin-bottom: 5px;
    }


    .subtitle {
        text-align: center;
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }


    .welcome-box {

        padding: 15px;
        border-radius: 12px;

        background-color: rgba(128,128,128,0.10);

        border: 1px solid rgba(128,128,128,0.25);

        text-align: center;

        line-height: 1.5;

        margin-bottom: 20px;
    }


    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Header
# ----------------------------

st.title("AskAI")

st.markdown(
    """
    <div class="subtitle">
    Your intelligent AI assistant for everyday questions.
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
# Welcome Screen
# ----------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-box">

        👋 <b>Welcome to AskAI</b>

        <br><br>

        Ask questions about coding, learning, writing, and more.

        <br><br>

        • Natural conversations  
        • Clear explanations  
        • Multi-topic assistance

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


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    # ----------------------------
    # Generate AI Response
    # ----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                prompt = f"""
You are AskAI, a natural conversational AI assistant.

Answer like a helpful human assistant.

Rules:
- Give the answer directly first.
- Keep normal answers around 5-10 lines.
- Give longer answers only when the user asks for details, steps, deep explanation, or complete guides.
- Do not start with phrases like "That's a great question", "Certainly", or similar expressions.
- Do not sound robotic or like a textbook.
- Avoid unnecessary headings.
- Use bullet points only when useful.
- Match the user's understanding level.
- Explain technical topics simply with examples.
- Keep simple questions simple.

User question:
{question}
"""


                response = model.generate_content(prompt)

                answer = response.text

                st.write(answer)


            except Exception:

                answer = (
                    "Sorry, I couldn't generate a response right now. "
                    "Please try again."
                )

                st.write(answer)



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
