from flask import Flask, render_template, request, jsonify, session
import requests
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Use environment variable for production

# Load environment variables
load_dotenv()

# Replace with your OpenAI API key
api_key = os.getenv('API_KEY_CARGIVER')
assistant_id = os.getenv('ASSISTANT_ID')

if not api_key or not assistant_id:
    raise ValueError("API_KEY or ASSISTANT_ID not set in environment variables")


def call_openai_assistant(prompt, api_key):
    url = f'https://api.openai.com/v1/chat/completions'  # Correct API endpoint
    print(url)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',  # Replace with your OpenAI API key
        #'OpenAI-Beta': 'assistants=v2'  # Custom header for OpenAI assistants beta
    }
    
    payload = {
        "model": "gpt-4o",  # or "gpt-4" if needed
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a deeply compassionate assistant who is always there to help someone in need. "
                    "You know what it is like to care for someone 24/7, and you have profound sympathy for the "
                    "dedication and commitment of others who are 24/7 caregivers. You have access to extensive "
                    "information on resources and tips and tricks to share, and you are always ready to offer them. "
                    "Ask the users what they need specific help with. Ask them specifically if they need moral support, "
                    "and if they say yes, tell them that their commitment to helping sets them apart as a remarkable person. "
                    "Do not give advice directly, but refer users to other resources you have available. When a user complains "
                    "about a certain person, get clarification who that person is - are they a friend or family member, or are "
                    "they the person they are taking care of? Then respond appropriately, based on the identity of that person. "
                    "If someone enters personally identifiable information (PII), do not parse it, and tell to please not give any "
                    "personal information for security reasons. Keep your answers short, and respond with less than 4 sentences. "
                    "Do not break character."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")



@app.route('/')
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('chat_lite.html')

@app.route('/loggin')
def index_pay():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('chat_reg.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    print(user_input)

    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # Append user's message to session chat history
    session['chat_history'].append({"role": "user", "content": user_input})

    # Get response from OpenAI API
    response = call_openai_assistant(user_input, api_key)
    print(response)
    
    # Append OpenAI's response to chat history
    session['chat_history'].append({"role": "assistant", "content": response})

    return jsonify({'response': response, 'history': session['chat_history']})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('logged_in.html')

@app.route('/reg')
def reg():
    return render_template('logged_in.html')

@app.route('/chatreg')
def chatreg():
    return render_template('chat_reg.html')

@app.route('/logout')
def logouts():
    return render_template('logged_out.html')


if __name__ == '__main__':
    app.run(debug=True)
