import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/tasks']

def get_tasks_service():
    creds = None
    base_path = os.path.dirname(__file__)
    token_path = os.path.join(base_path, 'tasks_token.json')
    credentials_path = os.path.join(base_path, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    service = build('tasks', 'v1', credentials=creds)
    return service

def list_tasks():
    service = get_tasks_service()
    results = service.tasks().list(tasklist='@default').execute()
    tasks = results.get('items', [])
    
    return tasks
def add_task(title, due=None, notes=None):
    service = get_tasks_service()
    task = {
        'title': title,
        'due': due,
        'notes': notes
    }
    
    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"Task '{title}' added with ID: {result['id']}")

list_tasks()