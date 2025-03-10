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
    cards = [
        {
            'heading': 'UncR',
            'subheading': 'Find your perfect unc!<br>Swipe ← for No &nbsp; Swipe → for Yes',
            'name': '',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png',
            'description': ''
        },
        {
            'heading': '',
            'subheading': '',
            'name': 'Suresh',
            'image': 'https://img.freepik.com/free-photo/indian-man-portrait-temple_53876-14535.jpg',
            'description': 'Loves feet'
        },
        {
            'heading': '',
            'subheading': '',
            'name': 'Niggesh',
            'image': 'https://i0.wp.com/journals-times.com/wp-content/uploads/2023/09/Rajessh-M-Iyer-photo.png',
            'description': 'likes little boys'
        }
    ]

    return render_template('index.html', cards=cards)



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