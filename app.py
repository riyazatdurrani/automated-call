import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import csv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/answer", methods=['POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Create TwiML response
    resp = VoiceResponse()
    
    # Use Gather to collect user input (speech)
    gather = Gather(input='speech', action='/process_speech', timeout=3, 
                    speech_timeout='auto', language='en-US')
    gather.say("Hello, my name is Firasat durrani. How can I help you today?")
    resp.append(gather)
    
    # If the user doesn't say anything, loop
    resp.redirect('/answer')
    
    return str(resp)

@app.route("/outgoing_call", methods=['POST'])
def outgoing_call():
    """Handle outgoing calls initiated by our system."""
    # Create TwiML response
    resp = VoiceResponse()
    
    # Get custom message if provided
    custom_message = request.values.get('message', None)
    
    if custom_message:
        resp.say(custom_message)
    else:
        # Default message
        resp.say("Hello, this is an automated call from Firasat Durrani's AI assistant. I'm calling to follow up with you.")
    
    # Use Gather to collect user input (speech)
    gather = Gather(input='speech', action='/process_speech', timeout=3,
                    speech_timeout='auto', language='en-US')
    gather.say("How can I help you today?")
    resp.append(gather)
    
    # If the user doesn't say anything, provide closure
    resp.say("I didn't hear a response. Thank you for your time. Goodbye.")
    
    return str(resp)

@app.route("/call_status", methods=['POST'])
def call_status():
    """Handle call status callbacks from Twilio."""
    # Get call details
    call_sid = request.values.get('CallSid', 'Unknown')
    call_status = request.values.get('CallStatus', 'Unknown')
    to_number = request.values.get('To', 'Unknown')
    
    # Log the call status
    with open('call_status_log.csv', 'a', newline='') as logfile:
        log_writer = csv.writer(logfile)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_writer.writerow([timestamp, call_sid, call_status, to_number])
    
    return "", 204  # No content response

@app.route("/process_speech", methods=['POST'])
def process_speech():
    """Process the caller's speech and respond with AI."""
    # Get the spoken text from the caller
    speech_result = request.values.get('SpeechResult', '')
    
    if speech_result:
        # Create a TwiML response
        resp = VoiceResponse()
        
        try:
            # Get response from OpenAI
            ai_response = get_ai_response(speech_result)
            
            # Convert the AI's text response to speech
            resp.say(ai_response)
        except Exception as e:
            # Handle errors gracefully
            resp.say("I'm sorry, I encountered an error while processing your request.")
            print(f"Error: {str(e)}")
        
        # Option to continue the conversation
        gather = Gather(input='speech', action='/process_speech', timeout=3,
                        speech_timeout='auto', language='en-US')
        gather.say("Is there anything else I can help you with?")
        resp.append(gather)
        
        # If they don't respond, end the call politely
        resp.say("Thank you for your time. Goodbye.")
        
        return str(resp)
    else:
        # If no speech was detected
        resp = VoiceResponse()
        resp.say("I didn't catch that. Let's try again.")
        
        gather = Gather(input='speech', action='/process_speech', timeout=3,
                        speech_timeout='auto', language='en-US')
        gather.say("")
        resp.append(gather)
        
        return str(resp)

def get_ai_response(user_input):
    """Get a response from OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful phone assistant. Your name is Firasat Durrani. Answer all questions in a friendly manner. Keep responses brief and conversational, suitable for phone calls."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return "I'm sorry, I'm having trouble connecting to my brain at the moment."

@app.route("/", methods=['GET'])
def index():
    """Display a simple homepage."""
    return "AI Phone Call System is running! Configure your Twilio webhook to point to /answer for incoming calls and /outgoing_call for outgoing calls."

if __name__ == "__main__":
    # Create call status log file if it doesn't exist
    if not os.path.exists('call_status_log.csv'):
        with open('call_status_log.csv', 'w', newline='') as logfile:
            log_writer = csv.writer(logfile)
            log_writer.writerow(['timestamp', 'call_sid', 'call_status', 'to_number'])
    
    # Run the Flask application
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 