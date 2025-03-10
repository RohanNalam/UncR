from flask import Flask, request, jsonify, render_template #type: ignore
from dotenv import load_dotenv #type: ignore
import os
from openai import OpenAI #type: ignore
import time

load_dotenv()


app = Flask(__name__)

# Configure OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY"),
)

@app.route('/')
def home():
    return render_template('index.html')
def message_ai(message):
    response = client.chat.completions.create(
        model="cognitivecomputations/dolphin3.0-mistral-24b:free",
        messages=[{
            "role": "system",
            "content": "Respond in a flirtatious way like you want to pursue a potential relationship. Utilize genZ slang."
        }, {
            "role": "user",
            "content": message
        }],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    while True:
        try:
            response = message_ai(user_message)
            break
        except Exception as e:
            print(f"ran into {e} retrying")
            time.sleep(3)

    return jsonify({'response': response})
    
    

if __name__ == '__main__':
    app.run(debug=True)