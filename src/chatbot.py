from langchain_openai import OpenAI
from langchain import ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from classification import classify_inquiry
from integrations.google_calendar import create_event, list_upcoming_events
from datetime import datetime, timedelta
import dateparser
from tasks.create_event_task import create_event_task
from tasks.send_email_task import send_email_task
from tasks.list_events_task import list_events_with_count
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM and today’s date
agent = OpenAI()
today_date = datetime.now().strftime("%Y-%m-%d")

# Memory setup with today's date context
memory = ConversationBufferMemory()
memory.chat_memory.add_user_message(
    f"Today is {today_date}. Use this date as the anchor point for interpreting any relative dates mentioned by the user, such as 'next Monday,' 'tomorrow,' or 'in two days.' Always consider {today_date} as 'today' throughout the conversation. Make sure that when you are comparing the years as well when considering relative dates."
)

conversation = ConversationChain(llm=agent, memory=memory)

end_chat_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Determine if the user input implies an intention to end the conversation.
User input = "{query}"
Answer with 'yes' if they want to end the conversation, or 'no' otherwise.
Answer:
"""
)
end_chat_chain = LLMChain(llm=agent, prompt=end_chat_prompt)

print("Chatbot: Hello! How can I assist you today?")

while True:
    query = input("You: ")

    category = classify_inquiry(query)
    print(category)
    if end_chat_chain.predict(query=query).strip().lower() == 'yes':
        print("Chatbot: Goodbye!")
        break

    if category == "Create Event":
        create_event_task(query)
    elif category == "List Events":
        list_events_with_count(query)
    elif category == "Send Email":
        send_email_task(query)
    else:
        response = conversation.predict(input=query)
        print(f"Chatbot: {response}")