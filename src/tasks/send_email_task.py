from integrations.gmail import send_email
from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI()

email_information_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are an assistant who prepares email details for sending. 
User input: "{query}"

Extract and format the email details as follows:
To: [Recipient's Email]
Subject: [Email Subject]
Message: [Email Body]

Details should include:
- **Recipient Email (To)**: Exact email address.
- **Message**: A polite, professional message body. Use formal language but avoid any placeholder values such as [Your Name]. Do not address the receiver unless name is given, and do not sign with sender's name unless name is given.
- **Subject**: A concise subject that summarizes the message of the email.

Return only the formatted response in three distinct lines.

Response:
"""
)

email_information_chain = LLMChain(llm=llm, prompt=email_information_prompt)

def send_email_task(query):
    response = email_information_chain.predict(query=query).strip()

    lines = response.splitlines()
    to = subject = message = None
    
    for line in lines:
        if line.startswith("To:"):
            to = line.split(":", 1)[1]
        elif line.startswith("Subject:"):
            subject = line.split(":", 1)[1]
        elif line.startswith("Message:"):
            message = line.split(":", 1)[1]

    send_email(to, subject, message)
    return response