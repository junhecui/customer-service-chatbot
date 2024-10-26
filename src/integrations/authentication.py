from google_calendar import get_calendar_service
from google_tasks import get_tasks_service
from gmail import get_gmail_service

# Authenticate Google APIs with authorized Google Account
if __name__ == "__main__":
    get_gmail_service()
    get_tasks_service()
    get_calendar_service()