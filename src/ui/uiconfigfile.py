from configparser import ConfigParser
import os

class Config:
    def __init__(self, config_file="./src/ui/uiconfigfile.ini"):
        self.config = ConfigParser()
        
        # Check if config file exists, if not use defaults
        if os.path.exists(config_file):
            self.config.read(config_file)
        else:
            # Set default values if config file doesn't exist
            self.config["DEFAULT"] = {
                "PAGE_TITLE": "Blog Generator with LangGraph AgenticAI",
                "LANGUAGE_OPTIONS": "English, Hindi, French",
                "TOPIC_SUGGESTIONS": "Agentic AI, Machine Learning, Web Development, Python, LangGraph, AI, Cloud Computing, Data Science"
            }

    def get_language_options(self):
        """Get available language options"""
        options_str = self.config["DEFAULT"].get("LANGUAGE_OPTIONS", "English, Hindi, French")
        return [opt.strip() for opt in options_str.split(",")]
    
    def get_topic_suggestions(self):
        """Get suggested blog topics"""
        topics_str = self.config["DEFAULT"].get("TOPIC_SUGGESTIONS", "Agentic AI, Machine Learning, Web Development")
        return [topic.strip() for topic in topics_str.split(",")]
    
    def get_page_title(self):
        """Get page title"""
        return self.config["DEFAULT"].get("PAGE_TITLE", "Blog Generator with LangGraph AgenticAI")
    
