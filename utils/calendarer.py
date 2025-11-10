from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('calendar', 'v3', credentials=creds)

def list_events():
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    items = events_result.get('items', [])
    return [f"{e['start'].get('dateTime', e['start'].get('date'))} – {e['summary']}" for e in items]

def add_event(title, start=None, hours=1):
    service = get_calendar_service()
    start_dt = start or datetime.utcnow()
    end_dt = start_dt + timedelta(hours=hours)
    event = {
        'summary': title,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/New_York'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/New_York'}
    }
    created = service.events().insert(calendarId='primary', body=event).execute()
    return f"✅ Event created: {created.get('htmlLink')}"
