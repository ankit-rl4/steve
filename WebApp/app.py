from flask import Flask, render_template, request, redirect, url_for, session
import requests
from chat import chat_response

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy credentials for demonstration
users = {'user1': 'password1'}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html')
    return redirect(url_for('login'))

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message']
    # Replace the following line with the actual API call to Azure ChatGPT model
    response = chat_response(user_message)
    return response


if __name__ == '__main__':
    app.run(debug=True)
