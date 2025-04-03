from outgoing_calls import make_call
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Your phone number (replace with your verified number)
to_number = "YOUR_VERIFIED_PHONE_NUMBER"  # Example: +1XXXXXXXXXX

# Make sure Twilio credentials are set
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
webhook_url = os.getenv("WEBHOOK_URL")

# Check for required variables
if not all([twilio_sid, twilio_token, twilio_number, webhook_url]):
    missing = []
    if not twilio_sid: missing.append("TWILIO_ACCOUNT_SID")
    if not twilio_token: missing.append("TWILIO_AUTH_TOKEN")
    if not twilio_number: missing.append("TWILIO_PHONE_NUMBER")
    if not webhook_url: missing.append("WEBHOOK_URL")
    
    print(f"Missing required environment variables: {', '.join(missing)}")
    print("Please update your .env file with these values.")
else:
    # Make the call
    message = "Hello, i am calling you from The Glamm Loft salon"
    call_sid = make_call(to_number, message)
    
    if call_sid:
        print(f"Call successfully initiated! Call SID: {call_sid}")
        print(f"The call will be made to {to_number}")
    else:
        print("Call failed to initiate. Check the error message above.")