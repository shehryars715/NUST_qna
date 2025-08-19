import streamlit as st
from qasystem import QASystem
from dotenv import load_dotenv

# Configuration
DOCUMENT_PATH = "data/data.pdf"  

def main():
    load_dotenv()
    
    st.set_page_config(
        page_title="NUST QA System",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 NUST QnA")
    st.markdown("Ask questions about NUST")
    
    # Initialize QA system
    if "qasystem" not in st.session_state:
        with st.spinner("Loading and processing document..."):
            st.session_state.qasystem = QASystem(DOCUMENT_PATH)
            st.session_state.qasystem.initialize()
    
    
    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Question input
    if question := st.chat_input("Ask a question about NUST"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context, response = st.session_state.qasystem.ask_question(question)
                
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()