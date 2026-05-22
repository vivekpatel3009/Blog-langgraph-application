from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self, api_key=None):
        load_dotenv()
        self.groq_api_key = api_key or os.getenv("GROQ_API_KEY")

    def get_llm(self):
        """
        Initialize and return the Groq LLM model.
        
        Returns:
            ChatGroq: The initialized LLM model
            
        Raises:
            ValueError: If API key is not provided or LLM initialization fails
        """
        try:
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is not provided or not found in environment variables")
            
            os.environ["GROQ_API_KEY"] = self.groq_api_key
            llm = ChatGroq(
                api_key=self.groq_api_key,
                model="llama-3.1-8b-instant",
                temperature=0.7
            )
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred initializing Groq LLM: {str(e)}")