from src.integrations.google_calendar import create_event, list_upcoming_events
from datetime import datetime, timedelta

def test_create_event():
    print("Testing create_event function...")
    summary = "Test Meeting"
    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    end_time = (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z'
    event = create_event(summary=summary, start_time=start_time, end_time=end_time)

def test_list_upcoming_events():
    print("Testing list_upcoming_events function...")
    events = list_upcoming_events(max_results=5)
    if events:
        print("Upcoming events:")
        for event in events:
            print(event['summary'], event['start'].get('dateTime', event['start'].get('date')))
    else:
        print("No upcoming events found.")


if __name__ == "__main__":
    test_create_event()
    test_list_upcoming_events()