from flask import Flask, request, render_template
import openai
import time

app = Flask(_name_)

# Set your OpenAI API key here
openai.api_key = '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'

# Store chat history in a list
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    # Check if the user's input is related to cybersecurity
    if is_cybersecurity_related(user_input)=="yes":
        response = chatbot_response(user_input)
        chat_history.append({'user': user_input, 'chatbot': response})
    else:
        response = "I'm sorry, but your question is not related to cybersecurity."

    return render_template('index.html', user_input=user_input, chatbot_response=response, chat_history=chat_history)

def chatbot_response(user_input):
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input,
                max_tokens=50,
                n=1,
                stop=None
            )
            if response.choices:
                return response.choices[0].text
            else:
                return "I'm sorry, but I couldn't generate a response to your question."
        except openai.error.RateLimitError as e:
            # Handle rate limit error by waiting for a brief moment
            time.sleep(5)  # Wait for 5 seconds and retry

def is_cybersecurity_related(user_input):
    # Construct the prompt with a direct question
    prompt = "Is this a cybersecurity-related query: " + user_input + " (yes/no)"

    # Get the chatbot's response
    response = chatbot_response(prompt)

    # Check if the response contains "yes"
    if "yes" in response.lower():
        return "yes"
    return "no"

if _name_ == '_main_':
    app.run(debug=True)
