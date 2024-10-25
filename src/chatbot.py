from langchain_openai import OpenAI
from langchain import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from classification import classify_inquiry

from dotenv import load_dotenv

load_dotenv()

agent = OpenAI()
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=agent,
    memory=memory
)

end_chat_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Determine if the user input implies an intention to end the conversation.
User input = "{query}"
Answer with 'yes' if they want to end the conversation, or 'no' otherwise.
Answer:
"""
)

end_chat_chain = LLMChain(
    llm=agent,
    prompt=end_chat_prompt
)

print("Chatbot: Hello! How can I assist you today?")
while True:
    query = input()

    category = classify_inquiry(query)
    # print(f"Debug: Classified as '{category}'")

    if end_chat_chain.predict(query=query) == 'yes':
        print("Chatbot: Goodbye!")
        break

    response = conversation.predict(input=query)
    print(f"Chatbot: {response}")