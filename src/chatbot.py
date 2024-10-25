from langchain_openai import OpenAI
from langchain import ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from classification import classify_inquiry
from integrations.google_calendar import create_event, list_upcoming_events
from datetime import datetime, timedelta
import dateparser
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM and today’s date
agent = OpenAI()
today_date = datetime.now().strftime("%Y-%m-%d")

# Memory setup with today's date context
memory = ConversationBufferMemory()
memory.chat_memory.add_user_message(f"Today's date is {today_date}. Remember this date for interpreting terms like 'next Monday' or 'tomorrow.'")

# Conversation chain with memory
conversation = ConversationChain(llm=agent, memory=memory)

# Prompt templates
end_chat_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Determine if the user input implies an intention to end the conversation.
User input = "{query}"
Answer with 'yes' if they want to end the conversation, or 'no' otherwise.
Answer:
"""
)

event_information_prompt = PromptTemplate(
    input_variables=["query", "today_date"],
    template="""
Today's date is {today_date}.
Extract the event details from the following user input:
User input: "{query}"

Please provide:
- Event Name (summary)
- Start Date and Time (start_time, in unicode format like 2024-10-25T10:00:00)
- End Date and Time (end_time, in unicode format like 2024-10-25T10:00:00)
List just the information out, separating each with commas.
Example: Meeting with Ted, 2024-10-25T10:00:00, 2024-10-25T11:00:00.
If given the day of the week, find today's day of the week and calculate the date that is being referred to based on today's date.
Example: If asked to book meeting on next Monday, find the date of the nearest Monday in the future and book the meeting then.

Output:
"""
)

event_count_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
User input = "{query}"

Please determine the number of events the user wants to see.
Answer with only the number.

For example:
- If a user says 'What is my next event?', return '1'
- If a user says 'What are my next two events?', return '2'
- If a user says 'What are my next events?', assume a default of 5 and return '5'
"""
)
end_chat_chain = LLMChain(llm=agent, prompt=end_chat_prompt)
event_count_chain = LLMChain(llm=agent, prompt=event_count_prompt)

def list_events_with_count(query):
    try:
        # Get the number of events to display
        num_events = int(event_count_chain.predict(query=query).strip())
        # print(f"Chatbot: Listing the next {num_events} events:")
        
        # Retrieve and print upcoming events
        events = list_upcoming_events(max_results=num_events)
        if events:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"Event: {event['summary']}, Start: {start}")
        else:
            print("Chatbot: No upcoming events found.")
    except Exception as e:
        print("Chatbot: An error occurred while fetching events:", e)


# Initialize LLM chains
end_chat_chain = LLMChain(llm=agent, prompt=end_chat_prompt)
event_information_chain = LLMChain(llm=agent, prompt=event_information_prompt)

print("Chatbot: Hello! How can I assist you today?")

while True:
    query = input("You: ")

    category = classify_inquiry(query)
    print(f"Debug: Classified as '{category}'")

    if end_chat_chain.predict(query=query).strip().lower() == 'yes':
        print("Chatbot: Goodbye!")
        break

    # Handle event creation if classified as 'Create Event'
    if category == "Create Event":
        extracted_details = event_information_chain.predict(query=query, today_date=today_date).strip()
        
        details = extracted_details.split(',')
        summary = details[0].strip() if len(details) > 0 else "Unknown Event"
        start_time_text = details[1].strip() if len(details) > 1 else "tomorrow at 12 PM"
        end_time_text = details[2].strip() if len(details) > 2 else ""

        start_time_parsed = dateparser.parse(start_time_text, settings={'PREFER_DATES_FROM': 'future'})
        if start_time_parsed is None:
            print(f"Chatbot: I couldn't understand the date '{start_time_text}'. Could you specify a clearer time?")
            continue

        start_time = start_time_parsed.isoformat()
        
        if end_time_text:
            end_time_parsed = dateparser.parse(end_time_text, settings={'PREFER_DATES_FROM': 'future'})
            end_time = end_time_parsed.isoformat() if end_time_parsed else (start_time_parsed + timedelta(hours=1)).isoformat()
        else:
            end_time = (start_time_parsed + timedelta(hours=1)).isoformat()

        print(f"Chatbot: Creating event '{summary}' from {start_time} to {end_time}.")
        event = create_event(summary=summary, start_time=start_time, end_time=end_time)
        print("Chatbot: Event created successfully!")
    elif category == "List Events":
        list_events_with_count(query)
        
    else:
        # General conversation fallback
        response = conversation.predict(input=query)
        print(f"Chatbot: {response}")