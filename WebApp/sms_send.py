import os
from twilio.rest import Client


def send_sms(to_phone_number, message_body):

    # Fetch environment variables
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    if not (twilio_phone_number and account_sid and auth_token):
        raise ValueError("Twilio credentials are not set in environment variables.")

    client = Client(account_sid, auth_token)

    # Send the message
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=to_phone_number
    )

    return message.sid


# Example usage
if __name__ == "__main__":
    recipient_phone_number = '+1234567890'
    message_body = 'Hello, this is a test message from the script!'
    try:
        message_sid = send_sms(recipient_phone_number, message_body)
        print(f"Message sent with SID: {message_sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")
