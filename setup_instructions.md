# AI Phone Call Automation Setup Instructions

## Prerequisites
1. A Twilio account with a phone number
2. An OpenAI API key
3. Python 3.7+ installed on your machine
4. ngrok for exposing your local server to the internet

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Edit the `.env` file and add your:
- OpenAI API key
- Twilio Account SID
- Twilio Auth Token

### 3. Test OpenAI Connection
Run the test script to verify your OpenAI API key is working:
```bash
python test_openai.py
```

### 4. Start the Flask Application
```bash
python app.py
```

### 5. Expose Your Local Server with ngrok
In a new terminal window:
```bash
ngrok http 5001
```

### 6. Configure Your Twilio Phone Number
1. Go to the Twilio Console
2. Navigate to Phone Numbers > Manage > Active Numbers
3. Click on your phone number
4. Under "Voice & Fax" section, find "A Call Comes In"
5. Set the webhook to your ngrok URL + "/answer" (e.g., https://your-ngrok-url.ngrok.io/answer)
6. Save your changes

### 7. Test Your System
Call your Twilio phone number to test the system. The AI should answer and respond to your queries.

## Troubleshooting
- If you encounter issues with Twilio webhooks, verify your ngrok URL is correct and your Flask app is running
- For OpenAI API errors, check your API key and ensure you have sufficient credits
- Make sure your port settings in the `.env` file match the port you're exposing with ngrok 

git init 

git add . 

git commit -m "Initial commit" 

git branch -M main 

git remote add origin https://github.com/riyazatdurrani/automated-call.git 

git push -u origin main 