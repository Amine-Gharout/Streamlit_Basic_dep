import streamlit as st
from langchain_groq import ChatGroq  # Interface to use Groq models

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from dotenv import load_dotenv

api_key= st.secrets["api_key"]

# Note: It's recommended to put this key in a .env file for security

# Initialize the Groq language model
llm = ChatGroq(api_key=api_key,
               model="llama-3.3-70b-versatile")  # Llama 3.3 70B model for high-quality responses

# System prompt that defines the AI assistant's behavior
SYSTEM_PROMPT = """
Speak always in French"""


def respond(conversation_history: list[BaseMessage]) -> str:
    # Create a proper message list with system message first
    messages = [SystemMessage(SYSTEM_PROMPT)] + conversation_history

    # Get response from the model
    response = llm.invoke(messages)

    # Don't add response to history here - let the calling code handle it
    # Return the response content with a newline
    return f"{response.content}\n"











if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tab name
st.set_page_config(page_title='Main', page_icon='😁')

st.title('Chatting')



for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message('Human'):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message('AI'):
            st.markdown(msg.content)






user_query = st.chat_input('prompt...')

if user_query is not None and user_query != '':
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message('Human'):
        st.markdown(user_query)

    with st.chat_message('AI'):
        response = respond(st.session_state.chat_history)
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(response))
