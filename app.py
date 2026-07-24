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
        padding: 18px;
        border-radius: 12px;
        background-color: white;
        border: 1px solid #ddd;
        margin-top: 20px;
        text-align: center;
        line-height: 1.6;
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
        AI assistant for:

        • Coding
        • Learning
        • Writing
        • General questions
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

        👋 Welcome to AskAI

        <br>

        Your AI assistant for coding, learning, writing, and everyday questions.

        <br>

        Ask anything and get clear, natural answers.

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


    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                prompt = f"""
You are AskAI, a natural conversational AI assistant.

Answer like a helpful human assistant.

Rules:
- Give the answer directly first.
- Keep normal answers around 5-10 lines.
- Give longer answers only when the user asks for details, steps, deep explanation, or a complete guide.
- Do not start with phrases like "That's a great question", "Certainly", or similar expressions.
- Do not sound robotic or like a textbook.
- Avoid unnecessary headings.
- Use bullet points only when they improve clarity.
- Match the user's level of understanding.
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



    # Save assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
