import os
from twilio.rest import Client
from dotenv import load_dotenv
import time
import csv
from datetime import datetime
import urllib.parse

# Load environment variables
load_dotenv()

# Initialize Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

def make_call(to_number, message=None, from_number=None):
    """
    Make an outgoing call to a specified number.
    
    Args:
        to_number (str): The phone number to call (E.164 format, e.g., +1XXXXXXXXXX)
        message (str, optional): Custom message for the call. Defaults to None.
        from_number (str, optional): The Twilio number to call from. Defaults to env variable.
    
    Returns:
        The call SID if successful, None otherwise
    """
    try:
        # Use the webhook URL for your AI response
        webhook_url = os.getenv("WEBHOOK_URL") + "/outgoing_call"
        
        # Add custom parameters if a message is provided
        if message:
            # URL encode the message and append it as a query parameter
            encoded_message = urllib.parse.quote(message)
            webhook_url = f"{webhook_url}?message={encoded_message}"
        
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=from_number or twilio_number,
            url=webhook_url,
            method="POST",
            status_callback=os.getenv("WEBHOOK_URL") + "/call_status",
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"]
        )
        
        print(f"Call initiated to {to_number}, Call SID: {call.sid}")
        return call.sid
    
    except Exception as e:
        print(f"Error making call: {str(e)}")
        return None

def batch_call(csv_file_path, delay_seconds=60):
    """
    Make calls to multiple numbers from a CSV file.
    
    CSV should have columns: phone_number, message (optional)
    
    Args:
        csv_file_path (str): Path to the CSV file with phone numbers
        delay_seconds (int): Delay between calls in seconds
    
    Returns:
        list: List of call SIDs for successful calls
    """
    call_sids = []
    log_file = f"call_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            with open(log_file, 'w', newline='') as logfile:
                log_writer = csv.writer(logfile)
                log_writer.writerow(['timestamp', 'phone_number', 'message', 'call_sid', 'status'])
                
                for row in reader:
                    phone_number = row.get('phone_number')
                    message = row.get('message', None)
                    
                    if phone_number:
                        # Make the call
                        call_sid = make_call(phone_number, message)
                        status = "initiated" if call_sid else "failed"
                        
                        # Log the call
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        log_writer.writerow([timestamp, phone_number, message, call_sid, status])
                        
                        if call_sid:
                            call_sids.append(call_sid)
                            
                        # Wait before making the next call
                        if delay_seconds > 0:
                            time.sleep(delay_seconds)
    
    except Exception as e:
        print(f"Error in batch call process: {str(e)}")
    
    print(f"Call log saved to {log_file}")
    return call_sids

def schedule_call(to_number, schedule_time, message=None):
    """
    Schedule a call for a future time using Twilio's scheduling features.
    
    Args:
        to_number (str): The phone number to call
        schedule_time (datetime): When to schedule the call
        message (str, optional): Custom message for the call
    
    Returns:
        The scheduled call SID if successful, None otherwise
    """
    try:
        # Format the schedule time for Twilio
        scheduled_time_str = schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Use the webhook URL for your AI response
        webhook_url = os.getenv("WEBHOOK_URL") + "/outgoing_call"
        
        # Add custom parameters if a message is provided
        if message:
            # URL encode the message and append it as a query parameter
            encoded_message = urllib.parse.quote(message)
            webhook_url = f"{webhook_url}?message={encoded_message}"
        
        # Schedule the call
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            url=webhook_url,
            method="POST",
            schedule_type="fixed",
            scheduled_time=scheduled_time_str,
            status_callback=os.getenv("WEBHOOK_URL") + "/call_status",
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"]
        )
        
        print(f"Call scheduled for {scheduled_time_str} to {to_number}, Call SID: {call.sid}")
        return call.sid
    
    except Exception as e:
        print(f"Error scheduling call: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    # 1. Make a single call
    # make_call("+1XXXXXXXXXX", "This is a test message")
    
    # 2. Make batch calls from a CSV file
    # batch_call("phone_numbers.csv", 60)
    
    # 3. Schedule a call for future time
    # from datetime import datetime, timedelta
    # schedule_time = datetime.utcnow() + timedelta(minutes=10)
    # schedule_call("+1XXXXXXXXXX", schedule_time, "This is a scheduled call")
    
    print("Run this file directly to make calls, or import the functions into another script.")
    print("Edit the main section to uncomment the examples you want to use.") 