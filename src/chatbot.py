from dotenv import load_dotenv
import warnings
import os
load_dotenv()
os.environ["PYTHONWARNINGS"] = os.getenv("PYTHONWARNINGS", "ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


from langchain_openai import OpenAI
from langchain import ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from classification import classify_inquiry
from datetime import datetime
import dateparser
from tasks.create_event_task import create_event_task
from tasks.send_email_task import send_email_task
from tasks.list_events_task import list_events_with_count
from tasks.answer_company_questions import retrieve_company_info
from tasks.create_todo_task import create_todo_task
from tasks.list_todo_task import list_todo_task
from tasks.google_search_task import google_search_task
from tasks.news_update_task import news_update_task
from tasks.recommend_place_task import recommend_place_task
from tasks.get_weather_task import get_weather_task

agent = OpenAI()

memory = ConversationBufferMemory()
today_date = datetime.now().strftime("%Y-%m-%d")
weekday = datetime.now().strftime("%A")
memory.chat_memory.add_user_message(
    f"Today is {weekday}, {today_date}. Use this date as the anchor point for interpreting any relative dates mentioned by the user, such as 'next Monday,' 'tomorrow,' or 'in two days.' Always consider {today_date} as 'today' throughout the conversation, and make sure the day of the week associated is correct. Make sure that when you are comparing the years as well when considering relative dates. Do not share this information when asked in a query."
)

conversation = ConversationChain(llm=agent, memory=memory)

end_chat_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Determine if the user input implies an intention to end the conversation. This is typically a sign of goodbye or that they are leaving.
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
    # print("Debug: " + category)

    if end_chat_chain.predict(query=query).strip().lower() == 'yes':
        print("Chatbot: Goodbye!")
        break

    if category == "Create Event":
        response = create_event_task(query)
    elif category == "List Events":
        response = list_events_with_count(query)
    elif category == "Send Email":
        response = send_email_task(query)
    elif category == "Company Information":
        response = retrieve_company_info(query)
    elif category == "Add Task":
        response = create_todo_task(query)
    elif category == "List Tasks":
        response = list_todo_task(query)
    elif category == "News Update":
        response = news_update_task(query)
    elif category == "Google Search":
        response = google_search_task(query)
    elif category == "Location Recommendations":
        response = recommend_place_task(query)
    elif category == "Weather Update":
        response = get_weather_task(query)
    else:
        response = conversation.predict(input=query)
    print(f"Chatbot: {response}")
    memory.chat_memory.add_user_message(query)
    memory.chat_memory.add_ai_message(response)