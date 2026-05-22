import uvicorn
from fastapi import FastAPI, Request, HTTPException
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Blog Generator API",
    description="Generate blog posts using LangGraph and Groq LLM",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "service": "Blog Generator API"}


@app.post("/blogs")
async def create_blogs(request: Request):
    """
    Create a blog post based on topic and optional language.
    
    Request body:
    {
        "topic": "str - The blog topic",
        "language": "str (optional) - Target language (english, hindi, french). Default: english",
        "api_key": "str - Groq API key"
    }
    
    Returns:
    {
        "success": bool,
        "data": {
            "blog": {
                "title": "str - Blog title",
                "content": "str - Blog content in markdown"
            },
            "language": "str - Language of the generated blog"
        },
        "message": "str - Status message"
    }
    """
    try:
        data = await request.json()
        topic = data.get("topic", "").strip()
        language = data.get("language", "english").lower()
        api_key = data.get("api_key", "").strip()
        
        # Validate inputs
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="GROQ API key is required")
        
        # Validate language
        supported_languages = ["english", "hindi", "french"]
        if language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language}' not supported. Supported languages: {', '.join(supported_languages)}"
            )
        
        # Initialize LLM
        groq_llm = GroqLLM(api_key=api_key)
        llm = groq_llm.get_llm()
        
        # Determine use case and build graph
        usecase = "language" if language != "english" else "topic"
        
        graph_builder = GraphBuilder(llm)
        graph = graph_builder.setup_graph(usecase=usecase)
        
        # Prepare input state
        input_state = {
            "topic": topic,
            "current_language": language
        }
        
        # Execute the graph
        result = graph.invoke(input_state)
        
        return {
            "success": True,
            "data": {
                "blog": {
                    "title": result["blog"].title,
                    "content": result["blog"].content
                },
                "language": language
            },
            "message": "Blog generated successfully"
        }
        
    except HTTPException as e:
        return {
            "success": False,
            "error": e.detail,
            "message": "Failed to generate blog"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "message": "LLM configuration error"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "An unexpected error occurred"
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

