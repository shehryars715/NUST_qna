# app.py
import streamlit as st
from search import retrieve_and_answer_query
import time

# Page config
st.set_page_config(
    page_title="NUST AI Chatbot", 
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom container */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* Title styling */
    .title-container {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 18px 18px 5px 18px;
        padding: 1rem 1.5rem;
        margin-left: 20%;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 18px 18px 18px 5px;
        padding: 1rem 1.5rem;
        margin-right: 20%;
        color: #2c3e50;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Input styling */
    .stChatInput {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stChatInput:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        outline: none;
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
        color: #667eea;
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        min-width: 150px;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #666;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px dashed #e0e0e0;
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.7;
    }
    
    /* Suggested questions */
    .suggestions-container {
        margin-top: 2rem;
        text-align: center;
    }
    
    .suggestion-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .suggestion-chip:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* Typing animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #667eea;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 3px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .chat-container {
            padding: 1rem;
            margin: 0 0.5rem 1rem 0.5rem;
        }
        
        .stChatMessage[data-testid="chat-message-user"] {
            margin-left: 10%;
        }
        
        .stChatMessage[data-testid="chat-message-assistant"] {
            margin-right: 10%;
        }
        
        .stat-card {
            min-width: 120px;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "show_typing" not in st.session_state:
    st.session_state.show_typing = False
if "latest_response" not in st.session_state:
    st.session_state.latest_response = ""

# Title Section
st.markdown("""
<div class="title-container">
    <div class="main-title">🤖 NUST AI Chatbot</div>
    <div class="subtitle">Your intelligent assistant for NUST information</div>
</div>
""", unsafe_allow_html=True)

# Stats Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.chat_history) // 2}</div>
        <div class="stat-label">Questions Asked</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Available</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">AI</div>
        <div class="stat-label">Powered</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">NUST</div>
        <div class="stat-label">Focused</div>
    </div>
    """, unsafe_allow_html=True)

# Chat Container
chat_container = st.container()

with chat_container:
    # Display welcome message if no chat history
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-message">
            <div class="welcome-icon">💬</div>
            <h3>Welcome to NUST AI Chatbot!</h3>
            <p>I'm here to help you with information about NUST. Feel free to ask me anything about admissions, programs, facilities, or general university information.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggested questions
        st.markdown("""
        <div class="suggestions-container">
            <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1rem;">💡 Try asking:</p>
            <div class="suggestion-chip">What programs does NUST offer?</div>
            <div class="suggestion-chip">How do I apply to NUST?</div>
            <div class="suggestion-chip">Tell me about NUST hostel charges</div>
            <div class="suggestion-chip">What are the admission requirements?</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for i, (role, message) in enumerate(st.session_state.chat_history):
        with st.chat_message(role):
            st.markdown(message)

# Chat Input
user_input = st.chat_input("💭 Ask me anything about NUST...")

if user_input:
    # Add user message immediately
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.message_count += 1
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Show typing indicator and get response
    with st.chat_message("assistant"):
        with st.spinner(""):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span>NUST Bot is typing</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                answer = retrieve_and_answer_query(user_input)
                # Add some personality to responses
                if "thank" in user_input.lower():
                    answer = "You're welcome! 😊 " + answer
                elif "hello" in user_input.lower() or "hi" in user_input.lower():
                    answer = "Hello! Welcome to NUST! 👋 " + answer
            except Exception as e:
                answer = f"❌ I'm sorry, I encountered an error while processing your question: {str(e)}. Please try again or rephrase your question."
            
            # Clear typing indicator and show response with typing effect
            typing_placeholder.empty()
            response_placeholder = st.empty()
            displayed_text = ""
            
            # Typing effect for new response
            for char in answer:
                displayed_text += char
                response_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.02)  # Adjust speed as needed
            
            # Final response without cursor
            response_placeholder.markdown(answer)
    
    # Add bot response to history
    st.session_state.chat_history.append(("assistant", answer))
    
    # Clear the input and rerun to show updated history
    st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.6);">
    <p>🎓 Powered by AI • Built for NUST Community • Made with ❤️ by Shehryar</p>
    <p style="font-size: 0.8rem;">© 2024 NUST AI Chatbot - Enhancing student experience through technology</p>
</div>
""", unsafe_allow_html=True)