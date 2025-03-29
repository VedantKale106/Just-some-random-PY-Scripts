"""import pywhatkit as kit
import time

# List of phone numbers (with country code)
numbers = ["+918421204009","+917028865256"]

# Message to send
message = "Hello! This is an automated message."

# Send messages
for number in numbers:
    kit.sendwhatmsg_instantly(number, message, wait_time=10)
    time.sleep(5)  # Sleep to avoid rate limiting"""

import pywhatkit as kit

kit.sendwhatmsg_instantly("+918421204009", "Hey, this is an automated message!", wait_time=10)

