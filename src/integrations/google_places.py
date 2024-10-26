import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY") 

def get_nearby_recommendations(longitude, latitude, search_type, radius=5000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": search_type,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    recommendations = []
    for place in results:
        name = place.get("name")
        address = place.get("vicinity")
        rating = place.get("rating")
        recommendations.append(f"{name}, {address} (Rating: {rating})")
    
    return recommendations if recommendations else "No recommendations found."