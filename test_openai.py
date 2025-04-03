import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_openai_connection():
    """Test the connection to the OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant, who is playing the role of the receptionist, answer to the questions from the user regading appointments  and give response as if you are the real person attending the client.give price in rupees if asked for price"},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=50
        )
        print("OpenAI API test successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"OpenAI API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection() 