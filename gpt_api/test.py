import requests

def test_chat_endpoint():
    url = "http://localhost:8000/chat"
    data = {"user_message": "Hello"}
    response = requests.post(url, json=data)
    print(response.text)

test_chat_endpoint()