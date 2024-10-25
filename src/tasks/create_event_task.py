from integrations.google_calendar import create_event
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
import dateparser
from datetime import datetime, timedelta

llm = OpenAI()

# Define event information prompt template
event_information_prompt = PromptTemplate(
    input_variables=["query", "today_date"],
    template="""
Today's date is {today_date}.
Extract the event details from the following user input:
User input: "{query}"

Please provide:
- Event Name (summary)
- Start Date and Time (start_time, in ISO format like 2024-10-25T10:00:00)
- End Date and Time (end_time, in ISO format like 2024-10-25T10:00:00)
List each item separately, separated by commas.
Example: Meeting with Ted, 2024-10-25T10:00:00, 2024-10-25T11:00:00.
If given a day of the week, calculate the date relative to today's date.

If the input lacks complete details, respond with "missing information".
"""
)

# LLMChain for extracting event information
event_information_chain = LLMChain(llm=llm, prompt=event_information_prompt)

def create_event_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    while True:
        extracted_details = event_information_chain.predict(query=query, today_date=today_date).strip()
        
        if "missing information" in extracted_details.lower():
            print("Chatbot: Could you specify the event name, start time, and end time?")
            query = input("You: ")
            continue
        
        details = extracted_details.split(',')
        if len(details) < 3:
            print("Chatbot: I couldn't understand all the details. Please provide event name, start time, and end time.")
            query = input("You: ")
            continue

        summary, start_time_text, end_time_text = details[0].strip(), details[1].strip(), details[2].strip()
        
        # Parse start and end times with error handling for None
        start_time_parsed = dateparser.parse(start_time_text, settings={'PREFER_DATES_FROM': 'future'})
        end_time_parsed = dateparser.parse(end_time_text) if end_time_text else (start_time_parsed + timedelta(hours=1))

        if not start_time_parsed:
            print("Chatbot: I couldn't understand the start time. Could you provide a clearer time?")
            query = input("You: ")
            continue
        
        # Format start and end times in ISO format
        start_time = start_time_parsed.isoformat()
        end_time = end_time_parsed.isoformat() if end_time_parsed else (start_time_parsed + timedelta(hours=1)).isoformat()

        # Try to create the event
        try:
            create_event(summary=summary, start_time=start_time, end_time=end_time)
            print("Chatbot: Event created successfully!")
            break
        except Exception as e:
            print(f"Chatbot: An error occurred while creating the event: {e}")
            break