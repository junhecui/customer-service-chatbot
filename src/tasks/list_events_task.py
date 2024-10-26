from integrations.google_calendar import list_upcoming_events
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

event_time_natural_prompt = PromptTemplate(
    input_variables=["query", "events", "today_date"],
    template="""
User input: "{query}"

Today's date is {today_date}.
You are given the following list of actual upcoming events: {events}.

Instructions:
1. If the user specifies a specific date (e.g., "events on October 30th"), provide only the events scheduled on that date in natural language, ordered by time.

2. If the user requests a certain number of upcoming events (e.g., "next 3 events"), provide that exact number of upcoming events in natural language.

3. If the user’s input is ambiguous (e.g., "what are my events?"), assume they want to know the next event.

4. If no events match the criteria, respond with "You have no events scheduled."

Return only one response that directly answers the user’s query based on the events provided.

Response:
"""
)

event_time_natural_chain = LLMChain(llm=llm, prompt=event_time_natural_prompt)

def list_events_with_count(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    events = list_upcoming_events()
    response = event_time_natural_chain.predict(query=query, events=events, today_date=today_date).strip()
    return response