from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(max_results=5):
    service = get_gmail_service()
    msgs = service.users().messages().list(userId='me', maxResults=max_results).execute().get('messages', [])
    snippets = []
    for m in msgs:
        full = service.users().messages().get(userId='me', id=m['id']).execute()
        snippets.append(full.get('snippet', '')[:150])
    return snippets
