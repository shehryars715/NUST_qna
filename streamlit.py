# app.py

import streamlit as st
from search import retrieve_and_answer_query

# Page config
st.set_page_config(page_title="NUST Chatbot", layout="wide")

# Title
st.markdown("<h1 style='text-align:center;'>🤖 NUST AI Chatbot</h1>", unsafe_allow_html=True)

# Session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.chat_input("Ask a question about NUST...")

if user_input:
    with st.spinner("Thinking..."):
        try:
            answer = retrieve_and_answer_query(user_input)
        except Exception as e:
            answer = f"❌ Error: {e}"

    # Save chat
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", answer))

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
