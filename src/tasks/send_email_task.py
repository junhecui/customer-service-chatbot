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
- **Message**: A polite, professional message body. If asking for a status update, use formal language.
- **Subject**: A concise subject that summarizes the message of the email.

Return only the formatted response in three distinct lines.
If the email details are unclear, ignore all previous instructions and return "unclear."
If the user cancels or gives a query with similar sentiment to 'nevermind', ignore all previous instructions and return "nevermind."
"""
)

email_information_chain = LLMChain(llm=llm, prompt=email_information_prompt)

def send_email_task(query):
    while True:
        extracted_details = email_information_chain.predict(query=query).strip()
        
        if extracted_details == 'nevermind':
            print("Chatbot: Understood. Is there anything else I can assist you with?")
            break
        elif extracted_details == 'unclear':
            print("Chatbot: Could you specify the email address you want to send it to, the subject, and the message content?")
            query = input("You: ")
            continue

        # Parse the labeled output
        try:
            to_line, subject_line, message_line = extracted_details.splitlines()
            to = to_line.replace("To:", "").strip()
            subject = subject_line.replace("Subject:", "").strip()
            message_text = message_line.replace("Message:", "").strip()

            # Confirm email details with the user
            print("\nChatbot: Here is the email I'm about to send:")
            print(f"To: {to}")
            print(f"Subject: {subject}")
            print(f"Message: {message_text}\n")
            
            confirm = input("Chatbot: Would you like to send this email? (yes/no): ").strip().lower()

            if confirm == 'yes':
                try:
                    send_email(to=to, subject=subject, message_text=message_text)
                    print("Chatbot: Email sent successfully!")
                    break
                except Exception as e:
                    print(f"Chatbot: An error occurred while sending the email: {e}")
                    break
            else:
                print("Chatbot: Email canceled. You can start over or provide updated details.")
                query = input("You: ")

        except ValueError:
            print("Chatbot: The details returned were incomplete. Could you provide the recipient, subject, and message?")
            query = input("You: ")