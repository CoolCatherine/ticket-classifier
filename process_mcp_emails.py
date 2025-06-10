import requests
from langchain_classifier import classify_with_langchain
from router import route_email

MCP_SERVER_URL = "http://localhost:5001/emails"

def fetch_emails_from_mcp():
    response = requests.get(MCP_SERVER_URL)
    if response.status_code == 200:
        return response.json().get('emails', [])
    else:
        print("Failed to fetch emails:", response.status_code)
        return []

def main():
    emails = fetch_emails_from_mcp()
    if not emails:
        print("No emails to process.")
        return

    for email in emails:
        print("-" * 40)
        print(f"Processing email from: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")
        #classify
        category = classify_with_langchain(email['subject'], email['body'])
        print(f"Classified as: {category}")
        #route
        result = route_email(category, email)
        print(f"Routing result: {result['status']} - {result['message']}")

if __name__ == "__main__":
    main()
