import chat_api
from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def parse(response):
    # Extract the response message
    response = json.loads(response)
    response_message = response['choices'][0]['message']['content']
    return response_message

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("user_message")
    response = chat_api.chat_response(user_message)
    return {"message": parse(response)}

@app.post("/personal_add")
async def personal_add(request: Request):
    data = await request.json()
    user_message = data.get("user_message")
    customer_id = data.get("customer_id")
    response = chat_api.generate_personalized_ad(customer_id)
    return response

@app.post("/sms_market")
async def sms_market(request: Request):
    data = await request.json()
    user_message = data.get("user_message")
    response = chat_api.sms_market(user_message)
    return response

@app.post("/phone_market")
async def phone_market(request: Request):
    data = await request.json()
    user_message = data.get("user_message")
    response = chat_api.phone_market(user_message)
    return response

@app.post("/email_market")
async def email_market(request: Request):
    data = await request.json()
    user_message = data.get("user_message")
    response = chat_api.email_market(user_message)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)