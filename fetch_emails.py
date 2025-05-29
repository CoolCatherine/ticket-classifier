import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Project defined categories
EMAIL_CATEGORIES = [
    "Technical Support",
    "Customer Support",
    "Product Feedback",
    "Compliance",
    "General Query"
]


API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it.")
genai.configure(api_key=API_KEY)

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Handles authentication flow to get Gmail service instance.
    """
    creds = None
    #load credentials from token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        #save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        #gmail API service
        service = build('gmail', 'v1', credentials=creds)
        return service

    except HttpError as error:
        print(f'An error occurred getting Gmail service: {error}')
        return None

def list_unread_messages(service):
    """Lists unread messages in the user's account.

    Args:
        service: Gmail API service instance.

    Returns:
        List of message dictionaries, or empty list on error.
    """
    try:
        #fetch unread messages
        results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
        messages = results.get('messages', [])
        return messages

    except HttpError as error:
        print(f'An error occurred listing messages: {error}')
        return []

def get_message_details(service, message_id):
    """Gets the details (sender, subject, body) of a message.

    Args:
        service: Gmail API service instance.
        message_id: ID of the message to retrieve.

    Returns:
        Dictionary containing sender, subject, and body, or None on error.
    """
    try:
        #message details
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        headers = message['payload']['headers']
        sender = 'Unknown Sender'
        subject = 'Unknown Subject'
        body = ''

        #extract sender and subject
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Subject':
                subject = header['value']

        #extracting body
        parts = message['payload'].get('parts')
        if parts:
            for part in parts:
               #search for plain text 
                if part['mimeType'] == 'text/plain' and 'body' in part:
                    body_data = part['body'].get('data')
                    if body_data:
                        body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                        break 
                
                elif 'body' in part and 'data' in part['body']:
                     body_data = part['body']['data']
                     body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    
        elif 'body' in message['payload'] and 'data' in message['payload']['body']:
             body_data = message['payload']['body']['data']
             body = base64.urlsafe_b64decode(body_data).decode('utf-8')


        return {'sender': sender, 'subject': subject, 'body': body}

    except HttpError as error:
        print(f'An error occurred getting message details: {error}')
        return None

def classify_email_with_gemini(subject, body, categories):
    """Classifies email based on subject and body using Gemini.

    Args:
        subject: Email subject string.
        body: Email body string.
        categories: List of possible categories.

    Returns:
        Predicted category string or None if classification fails.
    """
    try:
        #gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""Analyze the following email and classify it into one of the following categories:
{', '.join(categories)}

Email Subject: {subject}
Email Body:
{body}

Respond ONLY with the category name from the provided list. Do not include any other text or punctuation. If the content does not clearly fit any category, respond with '{categories[-1]}'.
"""

        response = model.generate_content(prompt)
        classification = response.text.strip()

        #classification 
        if classification in categories:
            return classification
        else:
            print(f"Warning: Gemini returned unexpected classification '{classification}'. Defaulting to '{categories[-1]}'.")
            return categories[-1] 
    except Exception as e:
        print(f"An error occurred during Gemini classification: {e}")
        return None 

if __name__ == '__main__':
  

    #gmail service
    service = get_gmail_service()

    if service:
        print("Successfully connected to Gmail API.")

        #list unread messages
        unread_messages = list_unread_messages(service)

        if not unread_messages:
            print("No unread messages found.")
        else:
            print(f"Found {len(unread_messages)} unread messages. Fetching details and classifying...")

            #process each unread message
            for msg in unread_messages:
                message_details = get_message_details(service, msg['id'])

                if message_details:
                    print("-" * 20)
                    print(f"Sender: {message_details['sender']}")
                    print(f"Subject: {message_details['subject']}")
                   
                    classification = classify_email_with_gemini(
                        message_details['subject'],
                        message_details['body'],
                        EMAIL_CATEGORIES
                    )


                    if classification:
                        print(f"Classified As: {classification}")
                    else:
                        print("Classification Failed.")

                    print("-" * 20)

       