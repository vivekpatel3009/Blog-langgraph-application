from src.states.blogstate import BlogState, Blog
from langchain_core.messages import SystemMessage, HumanMessage

class BlogNode:
    """
    A class to represent blog node operations in the LangGraph workflow.
    Handles title creation, content generation, and translation.
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        Create a title for the blog based on the topic.
        
        Args:
            state: The current state containing topic
            
        Returns:
            Updated state with blog title
        """
        if "topic" in state and state["topic"]:
            prompt = f"""You are an expert blog content writer. Generate a SINGLE blog title for the topic: {state['topic']}

Requirements:
- Return ONLY the title, nothing else
- Make it creative and SEO friendly
- Keep it concise (under 80 characters)
- Do NOT include alternatives or suggestions"""
            
            response = self.llm.invoke(prompt)
            title = response.content.strip()
            
            return {"blog": Blog(title=title, content="")}
        else:
            return {"blog": Blog(title="Untitled", content="")}
        
    def content_generation(self, state: BlogState):
        """
        Generate detailed blog content based on the topic and existing title.
        
        Args:
            state: The current state containing topic and blog title
            
        Returns:
            Updated state with blog content
        """
        if "topic" in state and state["topic"]:
            title = state["blog"].title if state.get("blog") else "Untitled"
            
            system_prompt = f"""You are an expert blog writer. Use Markdown formatting.
Generate a detailed and comprehensive blog content for the topic: {state['topic']}

Requirements:
- Write 3-5 sections with proper headings
- Include an introduction and conclusion
- Use markdown formatting (##, bold, lists, etc.)
- Make it informative and engaging
- Keep paragraphs concise and clear"""
            
            response = self.llm.invoke(system_prompt)
            content = response.content.strip()
            
            return {"blog": Blog(title=title, content=content)}
        else:
            return {"blog": Blog(title="Untitled", content="No content could be generated")}
        
    def translation(self, state: BlogState):
        """
        Translate both title and content to the specified language.
        
        Args:
            state: The current state containing blog and target language
            
        Returns:
            Updated state with translated blog content
        """
        current_language = state.get("current_language", "english").lower()
        
        # Skip translation if language is English
        if current_language == "english":
            return state
        
        blog_title = state["blog"].title
        blog_content = state["blog"].content
        
        # Translate title
        title_prompt = f"""Translate this blog title to {current_language}. 
Return ONLY the translated title, nothing else.
Title: {blog_title}"""
        
        title_response = self.llm.invoke(title_prompt)
        translated_title = title_response.content.strip()
        
        # Translate content
        content_prompt = f"""Translate this blog content to {current_language}.
- Keep markdown formatting
- Maintain tone and style
- Translate section headings appropriately
Return ONLY the translated content, nothing else.

Content: {blog_content}"""
        
        content_response = self.llm.invoke(content_prompt)
        translated_content = content_response.content.strip()
            
        return {"blog": Blog(title=translated_title, content=translated_content)}

    def route(self, state: BlogState):
        """
        Route node to prepare state for conditional routing.
        
        Args:
            state: The current state
            
        Returns:
            State with current_language field for routing
        """
        return {"current_language": state.get("current_language", "english")}
    
    def route_decision(self, state: BlogState):
        """
        Determine which translation path to take based on language.
        
        Args:
            state: The current state with language information
            
        Returns:
            String indicating the language path ("hindi", "french", or "english")
        """
        language = state.get("current_language", "english").lower()
        
        if language == "hindi":
            return "hindi"
        elif language == "french":
            return "french"
        else:
            return "english"