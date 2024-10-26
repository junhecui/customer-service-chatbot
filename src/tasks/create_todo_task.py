from integrations.google_tasks import add_task
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

todo_list_prompt = PromptTemplate(
    input_variables=["query", "today_date"],
    template="""
Today's date is {today_date}.
You are asked to add a task to a to-do list based on the following user input:
User input: "{query}"

If the user has indicated a task title but no due date, please respond with just the title.
Example:
User: Put 'take out the trash' on my to-do list.
Chatbot: take out the trash

If the user has indicated a task title and a due date but no additional details, please respond with the title and the date in ISO format, separated by a comma.
Example:
User: Put 'finish project' on my to-do list, due on October 30.
Chatbot: finish project, 2024-10-30

Response:
"""
)

todo_list_chain = LLMChain(llm=llm, prompt=todo_list_prompt)

def create_todo_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    response = todo_list_chain.predict(query=query, today_date=today_date)

    if ',' in response:
        title, due_date_str = map(str.strip, response.split(',', 1))
        due_date = datetime.fromisoformat(due_date_str).isoformat() + 'Z'
    else:
        title = response
        due_date = None
    
    if due_date:
        add_task(title, due_date)
    else:
        add_task(title)
    return response