from integrations.weather import get_weather_forecast
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

get_location_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are asked to give the longitude and latitude of the location present in the query.
User input: "{query}"

Return the response in the form: longitude, latitude, separated by a comma.

For example:
49.2859, -123.1249

Response:
"""
)

get_location_chain = LLMChain(llm=llm, prompt=get_location_prompt)

return_weather_prompt = PromptTemplate(
    input_variables=["query", "results", "today_date"],
    template="""
Today's date is "{today_date}"
    
Based on the given results, return the requested weather information given by the user input, phrased in natural language. The weather information should include temperature and precipitation, with precipitation interpreted in natural language (e.g., minimal rain, no rain).
Results: "{results}"
User input: "{query}"

For example:
- If the user asks what the weather is like today, give the weather information for the date that matches the current day.
- If the user asks what the weather is like for the next week, give the weather information for the next 7 days, including the current day.

Response:
"""
)

return_weather_chain = LLMChain(llm=llm, prompt=return_weather_prompt)

def get_weather_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    prediction = get_location_chain.predict(query=query)
    latitude, longitude = map(str.strip, prediction.split(","))
    forecast = get_weather_forecast(latitude, longitude)
    response = return_weather_chain.predict(query=query, results=forecast, today_date=today_date)
    return response