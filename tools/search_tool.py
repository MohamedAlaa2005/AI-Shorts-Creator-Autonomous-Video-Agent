import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

# Load environment variables (Make sure TAVILY_API_KEY is in your .env)
load_dotenv()

def get_search_tool():
    """
    Returns a configured Tavily search tool.
    In 2026, Tavily is preferred for agents due to its 
    high-speed, LLM-optimized results.
    """
    return TavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False # Keeping it False saves tokens/money
    )

# Quick test if run directly
if __name__ == "__main__":
    search = get_search_tool()
    results = search.invoke({"query": "Mohamed Salah latest news 2026"})
    print(results)