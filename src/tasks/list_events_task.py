from integrations.google_calendar import list_upcoming_events
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI()

# Define event count prompt template
event_count_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
User input = "{query}"
Determine the number of events the user wants to see.
Return only a single integer number.
For example:
- If a user says 'What is my next event?', return '1'
- If unspecified, assume '1'
- If a user says 'What are my next 4 events?', return '4'
"""
)

event_count_chain = LLMChain(llm=llm, prompt=event_count_prompt)

# Define prompt template to interpret the event time in natural language
event_time_natural_prompt = PromptTemplate(
    input_variables=["event_summary", "event_start_time"],
    template="""
Given the following event details:

- Event Name: {event_summary}
- Start Date and Time: {event_start_time} (ISO format)

Provide a natural language interpretation of when the event is happening, relative to the current date. For example, you might say "meeting is happening tomorrow at 3 PM" or "breakfast with family is next Monday at 10 AM".
Return only the natural language time description. Keep in mind what today's date is when stating relativity.
"""
)

event_time_natural_chain = LLMChain(llm=llm, prompt=event_time_natural_prompt)

def list_events_with_count(query):
    try:
        # Get number of events from the query
        count_result = event_count_chain.predict(query=query).strip()
        
        try:
            num_events = int(count_result)
        except ValueError:
            num_events = 1

        events = list_upcoming_events(max_results=num_events)
        
        if events:
            for event in events:
                event_summary = event['summary']
                event_start_time = event['start'].get('dateTime', event['start'].get('date'))

                natural_time_description = event_time_natural_chain.predict(
                    event_summary=event_summary,
                    event_start_time=event_start_time
                ).strip()

                print(f"Chatbot: {natural_time_description}")
        else:
            print("Chatbot: No upcoming events found.")
    except Exception as e:
        print("Chatbot: An error occurred while fetching events:", e)