"""
Streamlit UI for the Groq-powered chatbot.

Responsibilities:
- Manage chat session state (history of Human/AI messages)
- Render a simple chat interface with basic styling
- Stream assistant responses using Agent.respond_stream

Notes:
- Configure page title/icon via st.set_page_config.
- UI styling is applied via a small inline CSS block; tweak freely.
"""

import os
from langchain_groq import ChatGroq  # Interface to use Groq models
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from dotenv import load_dotenv
import streamlit as st
from Agent import respond_stream
# load_dotenv()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(
    page_title='AI Chat Assistant',
    page_icon='🤖',
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .stChatMessage {
        margin-bottom: 1rem;
    }
    .chat-stats {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 AI Chat Assistant</h1>',
            unsafe_allow_html=True)


# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message('Human'):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message('Ai'):
                st.markdown(msg.content)


# Chat input with modern styling
user_query = st.chat_input(
    "✨ Ask me anything...",
    key='chat_input'
)

# Handle new messages
if user_query:
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message('Human'):
        st.markdown(user_query)

    with st.chat_message('Ai'):
        with st.spinner('🤔 Thinking...'):
            response = st.write_stream(
                respond_stream(st.session_state.chat_history)
            )

    st.session_state.chat_history.append(AIMessage(response))
