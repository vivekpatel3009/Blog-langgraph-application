import streamlit as st
from src.states.blogstate import Blog

class DisplayResultStreamlit:
    def __init__(self):
        pass

    def display_result_on_ui(self, result):
        """
        Display the generated blog result on the Streamlit UI.
        
        Args:
            result: The state dictionary returned from the graph execution containing blog data
        """
        try:
            # Extract blog data from result
            blog_data = result.get("blog")
            
            if not blog_data:
                st.error("❌ Error: No blog data generated")
                return
            
            # Extract title and content - handle both dict and Pydantic model formats
            if isinstance(blog_data, dict):
                # If blog_data is a dictionary
                title = blog_data.get("title", "Untitled")
                content = blog_data.get("content", "No content generated")
            else:
                # If blog_data is a Pydantic model
                title = blog_data.title if hasattr(blog_data, "title") else "Untitled"
                content = blog_data.content if hasattr(blog_data, "content") else "No content generated"
            
            language = result.get("current_language", "english").upper()
            
            # Display blog title
            st.success("✅ Blog Generated Successfully!")
            st.markdown("---")
            
            # Language indicator
            st.markdown(f"**Language:** `{language}`")
            
            # Display blog title as heading
            st.markdown(f"# {title}")
            st.markdown("---")
            
            # Display blog content
            st.markdown(content)
            
            # Add download option
            st.markdown("---")
            
            # Create downloadable content
            blog_text = f"# {title}\n\n{content}"
            st.download_button(
                label="📥 Download Blog (Markdown)",
                data=blog_text,
                file_name=f"blog_{title.replace(' ', '_').lower()}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ Error displaying result: {str(e)}")
            import traceback
            st.error(traceback.format_exc())