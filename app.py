from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()


app = Flask(__name__)

# Replace with your OpenRouter API endpoint and key
OPENROUTER_API_URL = 'https://api.openrouter.ai/v1/chat'
OPENROUTER_API_KEY = os.getenv("API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

def message_ai(message):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
    extra_body={},
    model="mistralai/mistral-small-24b-instruct-2501:free",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"Here's the user's message[{message}] respond in a flirtatious way like you want to pursue a potential relationship."
            }
        ]
        }
    ]
    )
    response = completion.choices[0].message.content

    return response

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    while True:
        try:
            response = message_ai(user_message)
            break
        except Exception as e:
            print(f"ran into {e} retrying")

    return jsonify({'response': response})
    
    # # Prepare the payload for OpenRouter
    # payload = {
    #     'prompt': user_message,
    #     'max_tokens': 150
    # }
    
    # headers = {
    #     'Authorization': f'Bearer {OPENROUTER_API_KEY}',
    #     'Content-Type': 'application/json'
    # }
    
    # # Send the request to OpenRouter
    # response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    
    # if response.status_code == 200:
    #     ai_message = response.json().get('choices', [{}])[0].get('text', '').strip()
    #     return jsonify({'response': ai_message})
    # else:
    #     return jsonify({'error': 'Failed to get response from AI'}), 500

if __name__ == '__main__':
    app.run(debug=True)