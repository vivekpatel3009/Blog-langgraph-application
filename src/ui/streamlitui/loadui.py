import streamlit as st
import os

from src.ui.uiconfigfile import Config

@st.cache_resource
def get_ui_loader():
    """Cache the UI loader instance to prevent duplicate element creation."""
    return LoadStreamlitUI()

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()

    def load_streamlit_ui(self):
        """Load UI and return user controls from form inputs."""
        st.header("🤖 " + self.config.get_page_title())
        st.write("Generate blog content with AI powered by LangGraph and Groq LLM")

        with st.sidebar:
            st.subheader("📝 Blog Configuration")
            
            # Get options from config
            language_options = self.config.get_language_options()
            topic_options = self.config.get_topic_suggestions()
            
            # Topic input - either select from list or enter custom
            selected_topic = st.selectbox(
                "📌 Select Blog Topic", 
                options=topic_options,
                placeholder="Choose a topic or enter below",
                key="topic_selectbox"
            )
            
            custom_topic = st.text_input(
                "Or enter a custom topic:",
                placeholder="e.g., Agentic AI, Machine Learning, Web Development",
                key="custom_topic_input"
            )
            
            # Use custom topic if provided, otherwise use selected
            topic = custom_topic if custom_topic else selected_topic
            
            # Language selection
            selected_language = st.selectbox(
                "🌐 Select Language", 
                language_options,
                index=0,
                key="language_selectbox"
            )
            
            # API Key input
            st.subheader("🔑 API Configuration")
            groq_api_key = st.text_input(
                "GROQ API Key",
                type="password",
                help="Get your API key from https://console.groq.com/keys",
                key="groq_api_key_input"
            )
            
            if not groq_api_key:
                st.info("ℹ️ Please enter your GROQ API key to proceed. Get one at https://console.groq.com/keys")
            
            # Return user controls as dictionary
            user_controls = {
                "topic": topic,
                "selected_language": selected_language,
                "GROQ_API_KEY": groq_api_key
            }
        
        return user_controls