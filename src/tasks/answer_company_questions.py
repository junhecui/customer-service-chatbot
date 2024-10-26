import yaml
from langchain_openai import OpenAI
from langchain import LLMChain, PromptTemplate

# Initialize LLM
llm = OpenAI()

# Load YAML data and format as string
def load_and_format_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return yaml.dump(data)  # Convert YAML content to a string format for context

# Load company data
company_data_string = load_and_format_yaml("src/company_data.yaml")

# Define LLM prompt template
company_info_prompt = PromptTemplate(
    input_variables=["user_query", "company_data"],
    template="""
Company Data:
{company_data}

User Query: "{user_query}"

Based on the company data provided, find the most relevant information for the user's query. If the query does not match any available data, respond with "No specific company data found."

Examples:
User Query: "What are your operating hours?"
Response: "We operate from 8 AM to 8 PM on weekdays, and 9 AM to 5 PM on weekends."

User Query: "What internet plans do you offer?"
Response: "We offer three internet plans: Basic, Pro, and Premium, each tailored for different usage levels."

Response:
"""
)

company_info_chain = LLMChain(llm=llm, prompt=company_info_prompt)

# Function to respond to user queries
def retrieve_company_info(user_query):
    # Use LLM to find the best match based on YAML content and user query
    response = company_info_chain.predict(user_query=user_query, company_data=company_data_string).strip()
    return response