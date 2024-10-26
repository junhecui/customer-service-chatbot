import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_latest_headlines(keyword, language="en", num_results=5):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "language": language,
        "pageSize": num_results,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        results = []
        for article in articles:
            title = article["title"]
            url = article["url"]
            description = article.get("description", "No description available.")
            results.append(f"{title}\n{url}\n{description}")
        
        return "\n\n".join(results) if results else "No articles found."

    except requests.RequestException as e:
        return f"An error occurred: {e}"