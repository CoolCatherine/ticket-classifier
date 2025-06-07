import requests
import os
import json
from datetime import datetime

# Category to URL mapping (edit these URLs as needed)
CATEGORY_TO_URL = {
    "Technical Support": "https://company.com/api/support",
    "Customer Support": "https://company.com/api/customer",
    "Product Feedback": "https://company.com/api/feedback",
    "Compliance": "https://company.com/api/compliance",
    "General Query": "https://company.com/api/general",
    # Fallback URL for uncategorized/unknown
    "Fallback": "https://company.com/api/fallback"
}

LOG_FILE = "router_log.jsonl"  # Log file for processed emails

def route_email(category, email_payload):
    """
    Routes the email to the correct department based on category.
    Args:
        category (str): Classified category of the email.
        email_payload (dict): Email data (sender, subject, body, etc).
    Returns:
        dict: Result with status and message.
    """
    url = CATEGORY_TO_URL.get(category, CATEGORY_TO_URL["Fallback"])
    try:
        response = requests.post(url, json=email_payload, timeout=10)
        response.raise_for_status()
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category,
            "url": url,
            "email_payload": email_payload,
            "status": response.status_code,
            "response": response.text
        }
        log_action(log_entry)
        return {"status": "success", "message": f"Email routed to {category}", "url": url}
    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category,
            "url": url,
            "email_payload": email_payload,
            "status": "error",
            "error": str(e)
        }
        log_action(log_entry)
        return {"status": "error", "message": str(e), "url": url}

def log_action(entry):
    """Appends a log entry to the log file as JSONL."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# Example usage (for testing)
if __name__ == "__main__":
    test_email = {
        "sender": "user@example.com",
        "subject": "Cannot reset my password",
        "body": "I'm unable to reset my password and the link has expired."
    }
    result = route_email("Technical Support", test_email)
    print(result) 