import yaml
from langchain_openai import OpenAI
from langchain import LLMChain, PromptTemplate

llm = OpenAI()

def load_and_format_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return yaml.dump(data)

company_data_string = load_and_format_yaml("src/company_data.yaml")

company_info_prompt = PromptTemplate(
    input_variables=["user_query", "company_data"],
    template="""
Company Data:
{company_data}

User Query: "{user_query}"

Based on the company data provided, find the most relevant information for the user's query.

- If user is asking questions related to troubleshooting steps, guide them through the process step by step.

Examples:
User Query: "What are your operating hours?"
Response: "We operate from 8 AM to 8 PM on weekdays, and 9 AM to 5 PM on weekends." (no quotations)

User Query: "What internet plans do you offer?"
Response: "We offer three internet plans: Basic, Pro, and Premium, each tailored for different usage levels." (no quotations)

Do not write quotations in your answer.

Response:
"""
)

company_info_chain = LLMChain(llm=llm, prompt=company_info_prompt)

def retrieve_company_info(user_query):
    response = company_info_chain.predict(user_query=user_query, company_data=company_data_string).strip().replace('"', '')
    return response