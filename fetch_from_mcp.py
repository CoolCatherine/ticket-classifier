import requests

#url of MCP server
MCP_SERVER_URL = "http://localhost:5001/emails"

def fetch_emails():
    response = requests.get(MCP_SERVER_URL)
    if response.status_code == 200:
        emails = response.json().get('emails', [])
        print("Fetched emails:")
        for email in emails:
            print(f"From: {email['sender']}")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body']}")
            print("-" * 40)
    else:
        print("Failed to fetch emails:", response.status_code)

if __name__ == "__main__":
    fetch_emails()

