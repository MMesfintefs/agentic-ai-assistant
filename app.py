import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Agentic Assistant", layout="wide")

st.title("Agentic AI Assistant 🤖")
user_input = st.chat_input("Ask me anything…")

if user_input:
    with st.spinner("Thinking..."):
        answer = run_agent(user_input)
        st.chat_message("assistant").write(answer)
