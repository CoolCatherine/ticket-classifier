from flask import Flask, jsonify

app = Flask(__name__)

#emails
FAKE_EMAILS = [
    {
        'id': 1,
        'sender': 'user1@example.com',
        'subject': 'Cannot reset my password',
        'body': 'I am unable to reset my password and the link has expired.'
    },
    {
        'id': 2,
        'sender': 'user2@example.com',
        'subject': 'Feedback on your product',
        'body': 'I love your product, but I have some suggestions.'
    },
    {
        'id': 3,
        'sender': 'user3@example.com',
        'subject': 'Compliance question',
        'body': 'Is your service GDPR compliant?'
    },
    {
        'id': 4,
        'sender': 'user4@example.com',
        'subject': 'Issue with recent update',
        'body': 'After the latest update, the app crashes frequently.'
    },
    {
        'id': 5,
        'sender': 'user5@example.com',
        'subject': 'Request for refund',
        'body': 'I would like a refund for my last purchase. Please advise.'
    },
    {
        'id': 6,
        'sender': 'user6@example.com',
        'subject': 'Unable to login',
        'body': 'My account is locked and I cannot login. Please help.'
    },
    {
        'id': 7,
        'sender': 'user7@example.com',
        'subject': 'Feature request',
        'body': 'It would be great if your app could integrate with Google Calendar.'
    },
    {
        'id': 8,
        'sender': 'user8@example.com',
        'subject': 'Data privacy concern',
        'body': 'How do you handle user data and privacy?'
    },
    {
        'id': 9,
        'sender': 'user9@example.com',
        'subject': 'General inquiry',
        'body': 'What are your business hours?'
    },
    {
        'id': 10,
        'sender': 'user10@example.com',
        'subject': 'Customer support needed',
        'body': 'I was double charged for my subscription. Please assist.'
    },
    {
        'id': 11,
        'sender': 'user11@example.com',
        'subject': 'Broken link in email',
        'body': 'The link you sent me to verify my account does not work.'
    },
    {
        'id': 12,
        'sender': 'user12@example.com',
        'subject': 'Suggestion for improvement',
        'body': 'The user interface could be more intuitive.'
    },
    {
        'id': 13,
        'sender': 'user13@example.com',
        'subject': 'Legal inquiry',
        'body': 'Can you provide your terms of service and privacy policy?'
    },
    {
        'id': 14,
        'sender': 'user14@example.com',
        'subject': 'Thank you!',
        'body': 'Just wanted to say thanks for the great support last week.'
    },
    {
        'id': 15,
        'sender': 'user15@example.com',
        'subject': 'Account deletion request',
        'body': 'Please delete my account and all associated data.'
    }
]

@app.route('/emails', methods=['GET'])
def get_emails():
    return jsonify({'emails': FAKE_EMAILS})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    

