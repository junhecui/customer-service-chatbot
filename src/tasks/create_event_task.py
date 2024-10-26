from integrations.google_calendar import create_event
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
import dateparser
from datetime import datetime, timedelta

llm = OpenAI()

event_information_prompt = PromptTemplate(
    input_variables=["query", "today_date"],
    template="""
Today's date is {today_date}.
You are scheduling an event based on the following user input:
User input: "{query}"

Required details for event creation:
1. **Event Name**: a brief, specific summary of the event (e.g., "Meeting with Ted" if the query is "Book meeting with Ted").
2. **Start Date and Time**: the exact start date and time in ISO format (e.g., "2024-10-25T15:00:00").
3. **End Date and Time**: the exact end date and time in ISO format, or if not provided, calculated based on a duration after the start time (e.g., "1 hour after start").

**Instructions**:
- **Only respond** with: "Create event: <Event Name>, <Start Date and Time in ISO format>, <End Date and Time in ISO format>" if and only if all three details are present and correctly formatted.
- If **any required detail** is missing or unclear, such as the date, start time, or duration, respond with a specific request for the missing information. For example:
  - If the start time is missing: "Please provide the event start time."
  - If both the start and end times are missing: "Please provide the start time and either the end time or duration of the event."

Generate only one of the two responses:
- Either the exact "Create event" command with full details
- Or a specific request for the missing information.
"""
)

event_information_chain = LLMChain(llm=llm, prompt=event_information_prompt)

def create_event_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    response = event_information_chain.predict(query=query, today_date=today_date).strip()

    # Check if LLM has returned all required information to create the event
    if response.startswith("Create event:"):
        _, details = response.split("Create event:", 1)
        summary, start_time, end_time = [detail.strip() for detail in details.split(",")]

        create_event(summary=summary, start_time=start_time, end_time=end_time)

    return response