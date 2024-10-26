from langchain_openai import OpenAI
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()

classification_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Classify the following user input into one of the following categories: 
- Company Information: when the user wants information related to the company, such as services, policies, basic plan, standard plan, and premium plans, support hours, payment methods, or FAQs.
- Create Event: when the user wants to schedule a meeting, appointment, or any event on the calendar.
- List Events: when the user wants to see a list of upcoming events.
- Reminders: when the user wants to be reminded of something.
- Send Email: when the user wants to send a message or communicate with someone by sending an email to them.
- Location Recommendations: when the user asks for recommendations for locations nearby such as restaurants or malls.
- List Tasks: when the user wants to see their to-do list, or see their upcoming tasks.
- Add Task: when the user wants to add a task to their to-do list.
- News Update: when the user wants the latest news.
- Weather Update: when the user wants to know the weather.
- Google Search: when the user wants to search for information on the internet.

Examples:
- "Can you schedule a meeting with Ted tomorrow at 4 PM?" -> Create Event
- "Please remind me to send an email to Ted." -> Reminders
- "What's on my schedule for today?" -> List Events
- "Book a team meeting for next Friday." -> Create Event
- "Can you send a message to Ted?" -> Send Email
- "Can you tell me the company cancellation policy?" -> Company Information
- "Put 'take out the trash' on my to-do list." -> Add Task
- "What is the latest news on AI?" -> News Update
- "What is the current weather in Vancouver? -> Weather Update

User input: "{query}"
Category:
"""
)

classification_chain = LLMChain(
    llm=llm,
    prompt=classification_prompt
)

def classify_inquiry(query):
    response = classification_chain.predict(query=query).strip()
    return response.replace("- ", "")