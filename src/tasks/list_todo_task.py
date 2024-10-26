from integrations.google_tasks import list_tasks
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

todo_list_prompt = PromptTemplate(
    input_variables=["query", "tasks", "today_date"],
    template="""
Today's date is {today_date}.
You are asked to list the tasks from a to-do list based on the following to-do list and user input.
To-do list: "{tasks}"
User input: "{query}"

Based on what the user requests, return their upcoming tasks in natural language formatting.
For every task that is returned, return just the title and deadline.

- If the user asks to see their next task, return the first task with the closest upcoming deadline.
- The user could ask to see all of their tasks on a certain date.
- The user could ask to see all of their tasks.
- If the user asks if they have any tasks with a certain topic, search through the to-do list to see if they have any tasks that match the topic given, and return all that do.

Response:
"""
)

todo_list_chain = LLMChain(llm=llm, prompt=todo_list_prompt)

def list_todo_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    tasks = list_tasks()
    response = todo_list_chain.predict(query=query, tasks=tasks, today_date=today_date)
    return response