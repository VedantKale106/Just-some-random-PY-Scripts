from twilio.rest import Client

# Twilio credentials (get from Twilio console)
ACCOUNT_SID = "AC59aff6cf95ec28dc1538a69e00436e0f"
AUTH_TOKEN = "25bef53b1ac0a69852d44ca51bbb2617"
TWILIO_PHONE_NUMBER = "+18145930804"  # Twilio number

# List of phone numbers (with country code)
numbers = ["+918421204009"]

# Message to send
message_body = "HI Broo, Who is This?"

# Initialize Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Send messages
for number in numbers:
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=number
    )
    print(f"Message sent to {number}: {message.sid}")
