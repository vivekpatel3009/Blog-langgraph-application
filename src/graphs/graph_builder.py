from langgraph.graph import StateGraph, START, END
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.blog_node_obj = BlogNode(self.llm)

    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic only (English)
        """
        graph = StateGraph(BlogState)
        
        # Add nodes
        graph.add_node("title_creation", self.blog_node_obj.title_creation)
        graph.add_node("content_generation", self.blog_node_obj.content_generation)

        # Add edges
        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generation")
        graph.add_edge("content_generation", END)

        return graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language.
        Supports translation to Hindi and French.
        """
        graph = StateGraph(BlogState)
        
        # Add nodes
        graph.add_node("title_creation", self.blog_node_obj.title_creation)
        graph.add_node("content_generation", self.blog_node_obj.content_generation)
        graph.add_node("route", self.blog_node_obj.route)
        graph.add_node("hindi_translation", self.blog_node_obj.translation)
        graph.add_node("french_translation", self.blog_node_obj.translation)

        # Add edges
        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generation")
        graph.add_edge("content_generation", "route")

        # Add conditional edges based on language
        graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "hindi": "hindi_translation",
                "french": "french_translation",
                "english": END
            }
        )
        graph.add_edge("hindi_translation", END)
        graph.add_edge("french_translation", END)
        
        return graph

    def setup_graph(self, usecase="language"):
        """
        Setup and compile the appropriate graph based on use case.
        
        Args:
            usecase: "topic" for English-only blogs, "language" for multi-language support
            
        Returns:
            Compiled graph ready for execution
        """
        if usecase == "topic":
            graph = self.build_topic_graph()
        elif usecase == "language":
            graph = self.build_language_graph()
        else:
            # Default to language graph
            graph = self.build_language_graph()

        return graph.compile()

