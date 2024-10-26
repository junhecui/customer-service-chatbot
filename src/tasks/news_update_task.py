from integrations.news import fetch_latest_headlines
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from datetime import datetime

llm = OpenAI()

news_search_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are asked to summarize the following user query in a clear, succinct manner to be used for a news search.
User input: "{query}"

Response:
"""
)

news_search_chain = LLMChain(llm=llm, prompt=news_search_prompt)

news_results_prompt = PromptTemplate(
    input_variables=["query", "results", "today_date"],
    template="""
Today's date is "{today_date}"

Based on the news search results, return the result that closest answers the query, summarize it and post the summary followed by the link of the result.
Prioritize recent results, with heavy priority on stories that came out today.
Results: "{results}"
Query: "{query}"

Response:
"""
)

news_results_chain = LLMChain(llm=llm, prompt=news_results_prompt)

def news_update_task(query):
    today_date = datetime.now().strftime("%Y-%m-%d")
    to_search = news_search_chain.predict(query=query)
    results = fetch_latest_headlines(to_search)
    response = news_results_chain.predict(query=query, results=results, today_date=today_date)
    return response