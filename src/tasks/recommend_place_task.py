from integrations.google_places import get_nearby_recommendations
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

location_classification_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are asked to give the longitude and latitude of the location present in the query, as well as the place classification.
User input: "{query}"

The place classification must be one of the following:
accounting, airport, amusement_park, aquarium, art_gallery, atm, bakery, bank, bar, beauty_salon, bicycle_store, book_store, bowling_alley, bus_station, cafe, campground, car_dealer, car_rental, car_repair, car_wash, casino, cemetery, church, city_hall, clothing_store, convenience_store, courthouse, dentist, department_store, doctor, drugstore, electrician, electronics_store, embassy, fire_station, florist, funeral_home, furniture_store, gas_station, gym, hair_care, hardware_store, hindu_temple, home_goods_store, hospital, insurance_agency, jewelry_store, laundry, lawyer, library, light_rail_station, liquor_store, local_government_office, locksmith, lodging, meal_delivery, meal_takeaway, mosque, movie_rental, movie_theater, moving_company, museum, night_club, painter, park, parking, pet_store, pharmacy, physiotherapist, plumber, police, post_office, primary_school, real_estate_agency, restaurant, roofing_contractor, rv_park, school, secondary_school, shoe_store, shopping_mall, spa, stadium, storage, store, subway_station, supermarket, synagogue, taxi_stand, tourist_attraction, train_station, transit_station, travel_agency, university, veterinary_care, zoo

Return the response in the form: longitude, latitude, classification.

For example:
49.2859, -123.1249, restaurant

Response:
"""
)

location_classification_chain = LLMChain(llm=llm, prompt=location_classification_prompt)

recommendation_prompt = PromptTemplate(
    input_variables=["results"],
    template="""
Based on the given results, recommend the highest rated results to the user, giving the place name and address in natural language.
Results: "{results}"
Response:
"""
)

recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt)

def recommend_place_task(query):
    prediction = location_classification_chain.predict(query=query)
    longitude, latitude, classification = map(str.strip, prediction.split(","))
    results = get_nearby_recommendations(longitude, latitude, classification)
    response = recommendation_chain.predict(results=results)
    return response