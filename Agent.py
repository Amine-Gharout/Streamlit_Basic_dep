"""
Agent layer: initializes the Groq chat model via LangChain and exposes a
streaming response generator used by the Streamlit frontend.

Configuration (environment variables):
- GROQ_API_KEY: Your Groq API key (recommended to load from a .env file in dev).
- MODEL (optional): Model name from https://console.groq.com/docs/models.

Note: This file intentionally contains no business logic beyond constructing the
messages and streaming tokens. The Streamlit app composes/consumes it.
"""

from langchain_groq import ChatGroq  # Interface to use Groq models
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from typing import Iterator
from dotenv import load_dotenv
import os

# Load environment variables from a local .env file if present (development only).
# In production (e.g., Heroku), use Config Vars instead of a .env file.
load_dotenv()

# Read the Groq API key from the environment. Avoid hard-coding secrets in code.
api_key = os.getenv('GROQ_API_KEY')

# Initialize the Groq language model client. The model can be customized; see Groq docs
# for available model names and limits (tokens, rate limits, etc.).
llm = ChatGroq(
    api_key=api_key,
    model="model_name"  # Llama 3.3 70B model for high-quality responses
)
# System prompt that defines the AI assistant's behavior
SYSTEM_PROMPT = """
- Speck just french
- be crazy
- use emogies
"""


def respond_stream(conversation_history: list[BaseMessage]) -> Iterator[str]:
    """
    Stream assistant tokens given a conversation history.

    Parameters
    ----------
    conversation_history : list[BaseMessage]
        A list of LangChain messages (e.g., HumanMessage, AIMessage) representing
        the chat so far.

    Yields
    ------
    str
        Chunks of assistant content as they are produced. Suitable for
        `streamlit.write_stream` consumption.

    Notes
    -----
    - A SystemMessage with SYSTEM_PROMPT is prepended to steer the model's style.
    - This function does not mutate the passed conversation history.
    """
    # Prepend the system prompt to influence the assistant behavior.
    messages = [SystemMessage(SYSTEM_PROMPT)] + conversation_history
    # Stream partial tokens from the model and forward only content chunks.
    for chunk in llm.stream(messages):
        if getattr(chunk, "content", None):
            yield chunk.content
