from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""You are an expert blog content writer. Generate a SINGLE blog title for the topic: {topic}
            Requirements:
            - Return ONLY the title, nothing else
            - Make it creative and SEO friendly
            - Keep it concise (under 80 characters)
            - Do NOT include alternatives or suggestions"""
            
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self,state:BlogState):
        """
        Translate both title and content to the specified language separately.
        """
        print(f"Translating to : {state['current_language']}")
        blog_title = state["blog"]["title"]
        blog_content = state["blog"]["content"]
        
        # Translate title
        title_prompt = f"""Translate this blog title to {state['current_language']}. 
        Return ONLY the translated title, nothing else.
        Title: {blog_title}"""
        title_response = self.llm.invoke(title_prompt)
        translated_title = title_response.content.strip()
        
        # Translate content
        content_prompt = f"""Translate this blog content to {state['current_language']}.
        - Keep markdown formatting
        - Maintain tone and style
        Return ONLY the translated content, nothing else.
        Content: {blog_content}"""
        
        content_response = self.llm.invoke(content_prompt)
        translated_content = content_response.content.strip()
            
        return {"blog": {"title": translated_title, "content": translated_content}}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
            return state['current_language']