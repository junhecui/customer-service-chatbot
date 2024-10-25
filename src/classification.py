from langchain_openai import OpenAI
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()

classification_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Classify the following user input into one of the following categories: 
- Create Event: when the user wants to schedule a meeting, appointment, or any event on the calendar.
- List Events: when the user wants to see a list of upcoming events.
- Reminders: when the user wants to be reminded of something.
- Information Retrieval: when the user is asking for specific information.
- Send Email: when the user wants to send a message or communicate with someone by sending an email to them.
- Recommendations: when the user asks for suggestions or recommendations.
- General Assistance: for other types of help.

Examples:
- "Can you schedule a meeting with Ted tomorrow at 4 PM?" -> Create Event
- "Please remind me to send an email to Ted." -> Reminders
- "What's on my schedule for today?" -> List Events
- "Book a team meeting for next Friday." -> Create Event
- "Can you send a message to Ted?" -> Send Email

User input: "{query}"
Category:
"""
)

classification_chain = LLMChain(
    llm=llm,
    prompt=classification_prompt
)

def classify_inquiry(query):
    return classification_chain.predict(query=query).strip() # strip() to remove whitespace