import os

from flask import Flask, render_template, request, redirect, url_for, session, render_template_string

from gpt_api import chat_api
from gpt_api.chat_api import chat_response, generate_personalized_ad
import sqlite3
import json
from twilio.rest import Client


app = Flask(__name__)

app.secret_key = 'dummy'


conn = sqlite3.connect('users.db')


def parse(response):
    # Extract the response message
    response = json.loads(response)
    response_message = response['choices'][0]['message']['content']
    return response_message


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT email, Customer_ID FROM users WHERE email=? AND Password=?", (email, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = user[0]  # username
            session['customer_id'] = user[1]  # customer_id
            return redirect(url_for('chat'))
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'customer_id' in session:
        return render_template('chat.html')
    return redirect(url_for('login'))

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message']
    # Replace the following line with the actual API call to Azure ChatGPT model
    response = chat_response(user_message)
    return parse(response)



@app.route('/padd', methods=['GET','POST'])
def padd():
    # Replace the following line with the actual API call to Azure ChatGPT model
    response = generate_personalized_ad(session['customer_id'] )
    return response

@app.route('/marketer',methods = ['GET','POST'])
def marketer():
    return render_template('marketer.html')


@app.route('/distribution',methods = ['GET','POST'])
def distribution():
    return render_template('distribution.html')

@app.route('/send_sms', methods=['GET','POST'])
def send_sms():
    recipient_phone_number = '+919022698979'
    message_body = request.form['message']

    # Fetch environment variables
    twilio_phone_number = os.getenv('twilio_no')
    account_sid = os.getenv('twilio_sid')
    auth_token = os.getenv('twilio_auth')

    if not (twilio_phone_number and account_sid and auth_token):
        return "Twilio credentials are not set in environment variables.", 500

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )
        return render_template_string("""
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <title>Message Sent</title>
              </head>
              <body>
                <div class="container">
                  <h1 class="mt-5">Message Sent Successfully!</h1>
                  <p class="lead">Message SID: {{ message_sid }}</p>
                </div>
              </body>
            </html>
            """, message_sid=message.sid)
    except Exception as e:
        return f"Failed to send message: {e}", 500


@app.route('/sms_market',methods = ['GET','POST'])
def sms_market():
    user_message = request.form['message']
    # Replace the following line with the actual API call to Azure ChatGPT model
    response = chat_api.sms_market(user_message)
    return parse(response)

if __name__ == '__main__':
    app.run(debug=True)
