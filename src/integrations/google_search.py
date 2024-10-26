import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API credentials
API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY") 
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

def google_search(query, num_results=10):
    """Perform a Google search and return the results."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json().get("items", [])
        
        results = []
        for item in search_results:
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet")
            results.append(f"{title}\n{link}\n{snippet}")
        
        return "\n\n".join(results) if results else "No results found."
    
    except requests.RequestException as e:
        return f"An error occurred with the search: {e}"