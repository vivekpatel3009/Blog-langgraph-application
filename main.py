
import streamlit as st
import os
import requests
from src.ui.streamlitui.loadui import get_ui_loader
from src.llms.groqllm import GroqLLM
from src.graphs.graph_builder import GraphBuilder
from src.ui.streamlitui.display_result import DisplayResultStreamlit
from dotenv import load_dotenv
load_dotenv()
# Streamlit page configuration
st.set_page_config(
    page_title="🤖 Blog Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Determine if running against API or locally
BACKEND_URL = os.getenv("BACKEND_URL", "").strip()
USE_API = bool(BACKEND_URL)

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    Supports both local execution (direct graph) and remote API execution.
    
    The app takes topic and language as input and generates blog content using LangGraph.
    """

    # Load UI and get user inputs (cached to prevent duplicate elements)
    ui = get_ui_loader()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("❌ Error: Failed to load user input from the UI.")
        return
    
    # Check if required inputs are provided
    topic = user_input.get("topic")
    language = user_input.get("selected_language")
    groq_api_key = user_input.get("GROQ_API_KEY")

    if not topic:
        st.warning("⚠️ Please select or enter a blog topic to proceed.")
        return
    
    if not language:
        st.warning("⚠️ Please select a language.")
        return
    
    if not groq_api_key:
        st.warning("⚠️ Please enter your GROQ API key to proceed.")
        return

    # Show deployment info
    if USE_API:
        st.info(f"🌐 Using remote API: {BACKEND_URL}")
    else:
        st.info("💻 Running locally with direct graph execution")

    # Generate blog button
    if st.button("🚀 Generate Blog", key="generate_blog"):
        try:
            if USE_API:
                # Use remote API
                generate_blog_via_api(topic, language, groq_api_key)
            else:
                # Use local graph execution
                generate_blog_locally(topic, language, groq_api_key)

        except Exception as e:
            st.error(f"❌ Error: Blog generation failed - {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return


def generate_blog_via_api(topic: str, language: str, api_key: str):
    """
    Generate blog using remote API (for deployed version)
    
    Args:
        topic: Blog topic
        language: Target language
        api_key: Groq API key
    """
    try:
        with st.spinner("✨ Generating your blog..."):
            # Make API request
            response = requests.post(
                f"{BACKEND_URL}/blogs",
                json={
                    "topic": topic,
                    "language": language,
                    "api_key": api_key
                },
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    # Display the result
                    display_ui = DisplayResultStreamlit()
                    
                    # Convert API response to expected format
                    display_data = {
                        "blog": {
                            "title": result["data"]["blog"]["title"],
                            "content": result["data"]["blog"]["content"]
                        },
                        "current_language": result["data"]["language"]
                    }
                    
                    display_ui.display_result_on_ui(display_data)
                else:
                    st.error(f"❌ API Error: {result.get('error', 'Unknown error')}")
            else:
                error_data = response.json()
                st.error(f"❌ API Error ({response.status_code}): {error_data.get('detail', 'Unknown error')}")
                
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Blog generation took too long. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API: {BACKEND_URL}")
        st.info("Make sure the backend service is running and the URL is correct.")
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")


def generate_blog_locally(topic: str, language: str, api_key: str):
    """
    Generate blog using local graph execution (for development)
    
    Args:
        topic: Blog topic
        language: Target language
        api_key: Groq API key
    """
    try:
        with st.spinner("✨ Generating your blog..."):
            # Configure the LLM
            llm_config = GroqLLM(api_key=api_key)
            model = llm_config.get_llm()

            if not model:
                st.error("❌ Error: LLM model could not be initialized")
                return
            
            # Determine use case based on language selection
            usecase = "language" if language.lower() != "english" else "topic"
            
            # Build and run the graph
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(usecase)
            
            # Prepare state for graph execution
            input_state = {
                "topic": topic,
                "current_language": language.lower()
            }
            
            # Execute the graph
            result = graph.invoke(input_state)
            
            # Display the result
            display_ui = DisplayResultStreamlit()
            
            # Convert result to expected format
            display_data = {
                "blog": {
                    "title": result["blog"].title,
                    "content": result["blog"].content
                },
                "current_language": result.get("current_language", language.lower())
            }
            
            display_ui.display_result_on_ui(display_data)

    except Exception as e:
        st.error(f"❌ Error: Graph execution failed - {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return




if __name__ == "__main__":
    load_langgraph_agenticai_app()   
