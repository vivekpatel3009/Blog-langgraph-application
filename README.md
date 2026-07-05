# Blog Generator with LangGraph AgenticAI

An AI-powered blog generator built with LangGraph, Groq, Streamlit, and FastAPI. The app creates a blog title and full Markdown blog content from a topic, with optional translation support for Hindi and French.

## Features

- Generate SEO-friendly blog titles.
- Generate structured Markdown blog content with sections, introduction, and conclusion.
- Translate generated blogs to Hindi or French.
- Run locally through a Streamlit UI.
- Run as a FastAPI backend for API-based generation.
- Download generated blogs as Markdown from the UI.

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM (`llama-3.1-8b-instant`)
- Streamlit
- FastAPI
- Uvicorn
- Pydantic

## Project Structure

```text
blogAgentic/
+-- app.py                         # FastAPI backend
+-- main.py                        # Streamlit frontend
+-- requirements.txt               # Python dependencies
+-- src/
    +-- graphs/
    |   +-- graph_builder.py       # LangGraph workflow builder
    +-- llms/
    |   +-- groqllm.py             # Groq LLM configuration
    +-- nodes/
    |   +-- blog_node.py           # Graph nodes for title/content/translation
    +-- states/
    |   +-- blogstate.py           # Blog state and Pydantic models
    +-- ui/
        +-- uiconfigfile.ini       # UI options and defaults
        +-- streamlitui/
            +-- loadui.py          # Streamlit input controls
            +-- display_result.py  # Streamlit result display
```

## Requirements

- Python 3.11 or later
- Groq API key

Create a Groq API key from:

```text
https://console.groq.com/keys
```

## Setup

From the project folder:

```bash
cd blogAgentic
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Environment Variables

Create a `.env` file in the `blogAgentic` folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Optional, for making the Streamlit app call a remote FastAPI backend instead of running the graph locally:

```env
BACKEND_URL=https://blog-langgraph-application.onrender.com
```

If `BACKEND_URL` is not set, the Streamlit app runs the LangGraph workflow directly.

## Run the Streamlit App

```bash
streamlit run main.py
```

Then open the local Streamlit URL shown in the terminal.

In the UI:

1. Select a suggested topic or enter a custom topic.
2. Choose a language: English, Hindi, or French.
3. Enter your Groq API key.
4. Click **Generate Blog**.

## Run the FastAPI Backend

```bash
python app.py
```

The API runs on:

```text
https://blog-langgraph-application.onrender.com
```

Health check:

```bash
curl https://blog-langgraph-application.onrender.com/health
```

Generate a blog:

```bash
curl -X POST https://blog-langgraph-application.onrender.com/blogs ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"Agentic AI\",\"language\":\"english\",\"api_key\":\"your_groq_api_key_here\"}"
```

For PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "https://blog-langgraph-application.onrender.com/blogs" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"topic":"Agentic AI","language":"english","api_key":"your_groq_api_key_here"}'
```

## API Request Body

```json
{
  "topic": "Agentic AI",
  "language": "english",
  "api_key": "your_groq_api_key_here"
}
```

Supported languages:

- `english`
- `hindi`
- `french`

## API Response

```json
{
  "success": true,
  "data": {
    "blog": {
      "title": "Generated blog title",
      "content": "Generated blog content in Markdown"
    },
    "language": "english"
  },
  "message": "Blog generated successfully"
}
```

## How It Works

The LangGraph workflow uses a shared `BlogState` and runs through these steps:

1. `title_creation`: Generates a short, SEO-friendly title.
2. `content_generation`: Generates full Markdown blog content.
3. `route`: Checks the selected language.
4. `translation`: Translates the title and content when Hindi or French is selected.

For English blogs, the graph ends after content generation. For Hindi and French blogs, the generated English blog is translated before returning the result.

## Configuration

UI options are stored in:

```text
src/ui/uiconfigfile.ini
```

You can update:

- Page title
- Language options
- Suggested blog topics

## Notes

- Keep `.env` private and never commit API keys.
- `.venv`, `.env`, LangGraph runtime files, and local caches are ignored by `.gitignore`.
- The Streamlit app can run either directly against the local LangGraph workflow or through the FastAPI backend using `BACKEND_URL`.
