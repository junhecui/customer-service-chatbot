import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    base_path = os.path.dirname(__file__)
    token_path = os.path.join(base_path, 'token.json')
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

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, start_time, end_time, description=None, location=None):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': end_time, 'timeZone': 'America/Los_Angeles'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created:', event.get('htmlLink'))
    return event

def list_upcoming_events(max_results=10):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

get_calendar_service()