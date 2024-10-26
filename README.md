# Customer Service Chatbot for Internet Service Company

## Instructions

1. Clone this repository: <https://github.com/junhecui/customer-service-chatbot>.
2. Install all the requirements: `pip install -r requirements.txt`.
3. Create a `.env` file to store your OpenAI API key, Google Cloud key, Google Search Engine key, and News API key.
4. Run [`chatbot.py`](src/chatbot.py).

## Technologies Used

The bot is entirely built in Python primarily built with the LangChain framework utilizing the OpenAI API. 

## Understanding User Queries

Incoming user queries are classified into distinct categories in [classification.py](src/classification.py). These classifications are used for determining what task would like completed (such as sending an email, recommending restaurants or retrieving company information), and the respective LLM will be given the query based on the classification.

## Functionality

The agent is equipped with many features for task and inquiry support:

* Answering questions related to the Internet Service Company, such as their internet plans, billing information, troubleshooting steps, and frequently asked questions:

   > **You**: What internet plans does your company offer? <br>
   > **Chatbot**: We offer three internet plans: Basic, Standard, and Premium, each with different speeds and features to meet your needs.

* Send emails through Gmail. The bot will summarize a general message into a formal email:

   > **You**: Send an email to cjunhe05@gmail.com asking him if he has finished his project yet. <br>
   > **Chatbot**: To: cjunhe05@gmail.com <br>
   > Subject: Project Status <br>
   > Message: Dear recipient, I hope this email finds you well. I wanted to follow up and inquire if you have completed your project yet. I look forward to hearing from you. Thank you.

* Scheduling and viewing events with Google Calendar:

   > **You**: Schedule a meeting with Mark for tomorrow at 6pm. <br>

   > **You**: Do I have any events coming up? <br>
   > **Chatbot**: The next event is "Meeting with Mark" on October 26th at 6:00 PM.

* Add and view tasks on a to-do list with Google Tasks:

   > **You**: Remind me to take out the trash tomorrow. <br>

   > **You**: What does my to-do list look like? <br>
   > **Chatbot**: Your next task is "take out the trash" and it is due on 2024-10-27.

* Ask for highly rated location recommendations with Google Places:

   > **You**: Recommend me some restaurants on UBC.  
    > **Chatbot**:
    > 1. **Burgoo** - 4434 West 10th Avenue, Vancouver  
    > 2. **University Golf Club** - 5185 University Boulevard, Vancouver  
    > 3. **The Eatery** - 3431 West Broadway, Vancouver  
    > 4. **La Quercia & L'Ufficio** - 3689 West 4th Avenue, Vancouver  
    > 5. **The Mighty Oak @ the Well Cafe** - 5800 University Boulevard, Vancouver  
    > 6. **Jamjar Canteen** - 6035 University Boulevard, Vancouver  
    > 7. **Gallery Patio & Lounge** - 6133 University Boulevard 4th floor, Vancouver  
    > 8. **Browns Socialhouse Point Grey** - 3651 West 10th Avenue, Vancouver  
    > 9. **Koerner's Pub** - 1758 West Mall, Vancouver  
    > 10. **Ginger & Chili Restaurant** - 4409 West 10th Avenue, Vancouver

* Search for information with Google Search:

   > **You**: What does 'Natural Language Processing' mean? <br>
   > **Chatbot**: Natural Language Processing (NLP) is a technology that allows computers to understand and process human language in the form of text or speech. It involves converting this language into structured information that can be used by computers for various tasks. NLP is a subfield of computer science that has applications in business intelligence, media and communication, and many other fields.

* Stay up to date on the latest news:

   > **You**: News updates on McDonalds? <br>
   > **Chatbot**: "How McDonald's can learn from other fast-food giants in recovering from the deadly E. coli outbreak
    https://www.businessinsider.com/how-mcdonalds-can-recover-from-food-safety-crisis-e-coli-2024-10
    Chipotle faced a similar food-safety crisis in 2015 and 2016, but managed to bounce back less than five years later.

* Get weather updates:

   > **You**: How is the weather in Vancouver today? <br>
   > **Chatbot**: The temperature in Vancouver for today (2024-10-26) is expected to range from 10.2°C to 14.1°C with a total of 6.5 mm of precipitation. There is a chance of minimal rain today.

## API Integration

The following API integrations were used to perform the various functionalities: Gmail, Google Calendar, Google Places, Google Search, Google Tasks, News, Meteo Weather.

## Escalation to Human Assistance

There has not been implementation for escalation to human assistance. The mechanism for escalating to human agents would likely be used for answering questions related to the company, particularly during troubleshooting. [company_data.yaml](src/company_data.yaml) currently has steps for various troubleshooting problems; during conversation with a user, the bot would go through all the troubleshooting steps for a particular issue, and if it is not resolved by the last troubleshooting step, a mechanism could be implemented to transfer to human agents at that point. Furthermore, the bot could also transfer users to human agents when asked a query that is classified as a company related question, but the answer is not in the available company data.

To reduce the amount of transferring to human agents needed, the bot should have access to company data for all common questions.

## Key Performance Indicators:

### Reliability

Reliability would measure how accurately the bot completes the intended tasks and answers the correct questions. Currently, the bot is somewhat reliable at performing various tasks, but it is recommended that the user inputs all the necessary information to complete a task in one message, as the bot struggles with calling on APIs with data obtained from multiple queries. For example, if a user wanted to send an email, it is recommended that they include the address and general message in one query. This is also recommended for reducing operational costs of running multiple queries. This is an area of improvement, where the bot's memory could be improved to specifically remember pertinent information for a task until that task is completed.

### Speed

Speed would measure how quickly the bot responds and completes tasks. Overall, the bot's speed is very quick, as most tasks and responses are given within less than a second, with some slower tasks (finding news articles, place recommendations) taking a few seconds at maximum. This would still be significantly faster than a human agent.

### Operational Cost

Operational cost would measure the cost it takes to run the bot as well as the various APIs it calls on. The cost of running the OpenAI LLM itself is not very high, as it takes multiple queries per cent of operational costs, but some APIs used are expensive when scaled up. For building and testing purposes, I have not incurred any costs of these APIs, but on a mass scale, APIs such as Places API and Google Custom Search cost around $5-20 dollars per thousand requests.

### Human Resource Requirement

Depending on how much company information the bot has access to, the human resource requirement could vary. Based on the proposed mechanism for transferring to human agents above, I suspect that the primary area for incurring human resources would be for specific troubleshooting help.
