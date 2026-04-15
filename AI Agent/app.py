"""Streamlit web app for the SimpleAIAgent."""

import html
import os
import re

import streamlit as st
from dotenv import load_dotenv

from agent import SimpleAIAgent


load_dotenv()


st.set_page_config(
    page_title="LLM chat Bot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .topic-line {
        margin: 0.2rem 0;
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
        font-size: 1.05rem;
        line-height: 1.45;
    }
    .topic-label,
    .topic-value {
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def style_topic_subtopic_lines(content: str) -> str:
    """Apply custom font styling to topic and subtopic lines."""
    pattern = re.compile(
        r"^\s*(?:[-*]\s+)?\*{0,2}(topic|subtopic)\*{0,2}\s*[:\-]\s*\*{0,2}(.*?)\*{0,2}\s*$",
        re.IGNORECASE,
    )
    styled_lines = []

    for line in content.splitlines():
        match = pattern.match(line)
        if match:
            label = html.escape(match.group(1).title())
            value = html.escape(match.group(2).strip())
            styled_lines.append(
                f'<p class="topic-line"><span class="topic-label">{label}:</span> '
                f'<span class="topic-value">{value}</span></p>'
            )
        else:
            styled_lines.append(line)

    return "\n".join(styled_lines)


def get_agent(system_prompt: str) -> SimpleAIAgent:
    agent = st.session_state.get("agent")
    current_prompt = st.session_state.get("system_prompt")

    if agent is None or current_prompt != system_prompt:
        agent = SimpleAIAgent(system_prompt=system_prompt)
        st.session_state.agent = agent
        st.session_state.system_prompt = system_prompt

    return agent


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("Controls")
    st.caption("Configure the agent before sending messages.")

    api_key_present = bool(os.getenv("GROQ_API_KEY"))
    if api_key_present:
        st.success("GROQ_API_KEY detected")
    else:
        st.warning("Set GROQ_API_KEY before chatting")

    system_prompt = st.text_area(
        "System prompt",
        value="""You are a helpful AI agent designed to assist with various tasks.
You can help with:
- Answering questions
- Generating ideas and solutions
- Writing and editing content
- Analyzing information
- Solving problems step by step

Be clear, concise, and helpful in your responses.
When mentioning topic or subtopic, format both label and value in bold markdown.
Example:
**Topic:** **Python**
**Subtopic:** **Error Handling**""",
        height=220,
    )

    model_options = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]
    selected_model = st.selectbox("Conversation model", options=model_options, index=0)
    custom_model = st.text_input("Custom model (optional)", value="")
    model = custom_model.strip() or selected_model

    temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.05)
    max_tokens = st.slider("Max tokens", min_value=64, max_value=2048, value=512, step=64)
    history_window = st.slider("History window", min_value=1, max_value=20, value=8, step=1)

    if st.button("Clear conversation", use_container_width=True):
        if "agent" in st.session_state:
            st.session_state.agent.clear_history()
        st.session_state.messages = []
        st.rerun()


st.markdown(
    """
    <h1>LLM chat Bot</h1>
    <p>A Streamlit chat interface for the Groq-powered agent. Keep context across turns, tune generation settings, and switch prompts from the sidebar.</p>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []


if st.session_state.messages:
    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                st.markdown(style_topic_subtopic_lines(message["content"]), unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
else:
    st.info("Start a new thread by asking a question below.")


user_prompt = st.chat_input("Ask the agent something")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    try:
        agent = get_agent(system_prompt)
        with st.spinner("Thinking..."):
            response = agent.execute_task(
                user_prompt,
                temperature=temperature,
                model=model or None,
                max_tokens=max_tokens,
                history_window=history_window,
            )

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    except Exception as error:
        error_message = f"Unable to generate a response: {error}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.rerun()

