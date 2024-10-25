from langchain_openai import OpenAI
from langchain import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()

classification_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Classify the following user input into one of the following categories: Scheduling, Reminders, Information Retrieval, Task Management, Communication, Recommendations, General Assistance

User input: "{query}"
Category:
"""
)

def classify_inquiry(query):
    return llm(classification_prompt.format(query=query)).strip() # strip() to remove whitespace