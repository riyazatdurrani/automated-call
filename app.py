import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from dotenv import load_dotenv

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
        resp.redirect('/answer')
        
        return str(resp)
    else:
        # If no speech was detected
        resp = VoiceResponse()
        resp.say("I didn't catch that. Let's try again.")
        resp.redirect('/answer')
        
        return str(resp)

def get_ai_response(user_input):
    """Get a response from OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful phone assistant.your name is Firasat Durrani. and you answer all the questions in a friendly manner."},
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
    return "AI Phone Call System is running! Configure your Twilio webhook to point to /answer"

if __name__ == "__main__":
    # Run the Flask application
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 