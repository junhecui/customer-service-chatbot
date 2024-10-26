from integrations.google_search import google_search
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

google_search_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are asked to summarize the following user query in a clear, succinct manner to be used for a google search.
User input: "{query}"

Response:
"""
)

google_search_chain = LLMChain(llm=llm, prompt=google_search_prompt)

google_search_results_prompt = PromptTemplate(
    input_variables=["query", "results"],
    template="""
Based on the google search results, return the result that closest answers the query, summarize it and post the summary followed by the link of the result.
Results: "{results}"
Query: "{query}"

Response:
"""
)

google_search_results_chain = LLMChain(llm=llm, prompt=google_search_results_prompt)

def google_search_task(query):
    to_search = google_search_chain.predict(query=query)
    results = google_search(to_search)
    print(results)
    response = google_search_results_chain.predict(query=query, results=results)
    return response