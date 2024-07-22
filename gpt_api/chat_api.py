import os
import sqlite3

import PyPDF2
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider,InteractiveBrowserCredential
from config import ENDPOINT, KEYAPI
import json
# Fetch endpoint and deployment name from environment variables or config
endpoint = os.getenv("ENDPOINT_URL", "https://steve2000.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "steve8k")
keyapi = os.getenv("AZURE_OPENAI_API_KEY")

# Authenticate using InteractiveBrowserCredential
credential = InteractiveBrowserCredential()

# Get bearer token provider

try:
    # Initialize AzureOpenAI client
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_version="2024-05-01-preview",
        api_key=keyapi
    )
except Exception as e:
    print(f"Error initializing AzureOpenAI client: {e}")



rag_doc = {
    'offers': [
        {'product': 'Personal Loan', 'interest_rate': 10.99, 'processing_fee': 1.5},
        {'product': 'Credit Card', 'cashback': 5, 'annual_fee': 500},
        {'product': 'Home Loan', 'interest_rate': 8.5, 'processing_fee': 0.5},
        {'product': 'Car Loan', 'interest_rate': 12.99, 'processing_fee': 1},
        {'product': 'Fixed Deposit', 'interest_rate': 7, 'minimum_deposit': 10000},
        {'product': 'SIP', 'return_rate': 12, 'minimum_investment': 500},
        {'product': 'Insurance', 'coverage': 1000000, 'premium': 5000}
    ]
}

def chat_response(user_message):
    # Open the PDF file
    pdf_file = open('RAG_DATA/gov.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the text from the PDF file
    pdf_text = ''
    for page in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page].extract_text()

    # Create chat completion request
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a customer service representative from Bank of Baroda. Please reply to customer requests using polite and respectful language. You have access to the following information from the Government Schemes PDF: " + pdf_text},
            {"role": "user", "content": user_message}
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    # Close the PDF file
    pdf_file.close()

    return completion.to_json()

def generate_personalized_ad(customer_id):
    # Retrieve salary and interested product from the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            last_3months_personal_loan_inq, 
            last_3months_credit_card_inq, 
            last_3months_home_loan_inq, 
            last_3months_car_loan_inq, 
            last_3months_fixed_deposit_inq, 
            last_3months_sip_inq, 
            last_3months_insurance_inq 
        FROM 
            users 
        WHERE 
            Customer_ID = ?
    """, (customer_id,))

    row = cursor.fetchone()

    interested_products = []

    if row:
        products = {
            'Personal Loan': row[0],
            'Credit Card': row[1],
            'Home Loan': row[2],
            'Car Loan': row[3],
            'Fixed Deposit': row[4],
            'SIP': row[5],
            'Insurance': row[6]
        }

        for product, interested in products.items():
            if interested:
                interested_products.append(product)
    cursor.execute("""
        SELECT 
            'Annual Income' 
        FROM 
            users 
        WHERE 
            Customer_ID = ?
    """, (customer_id,))

    salary = cursor.fetchone()[0]


    # Create a prompt for the GenAI API chat completion
    prompt = f"Generate a personalized ad of not more than 20 words for a customer interested in {interested_products} with a salary of {salary}. Use the following RAG document: {json.dumps(rag_doc)}"

    # Generate a personalized ad using the GenAI API chat completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    # Parse the completion response
    response = completion.to_json()
    ad = json.loads(response)['choices'][0]['message']['content']
    conn.close()
    return ad



def sms_market(user_message):
    pdf_file = open('RAG_DATA/sms_mark.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the text from the PDF file
    pdf_text = ''
    for page in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page].extract_text()

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system",
             "content": "As a marketer at Bank of Baroda, please generate a short SMS ad targeting customers interested in product/service. The message should be brief, highlighting the key offer and a call to action in no more than two lines. You have access to the following information from the sms marketing PDF: " + pdf_text + "and current offers" + json.dumps(rag_doc)},
            {"role": "user", "content": user_message}
        ]
,
    max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return completion.to_json()

def phone_market(user_message):
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system",
             "content": "As a marketer at Bank of Baroda, please generate a short phone call script targeting customers interested in  product/service. The script should be concise, highlighting the key offer and encouraging the customer to take action, all within two lines."},
            {"role": "user", "content": user_message}
        ]
,
    max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return completion.to_json()

def email_market(user_message):
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system",
             "content": "As an email marketer at Bank of Baroda, please generate a personalized email ad targeting customers interested in product/service. The email should emphasize the unique benefits and exclusive offers we provide, and should be structured as follows: [Introduction, Offer Details, Benefits, Call to Action, Conclusion]."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return completion.to_json()


# Example usage:
if __name__ == "__main__":
    user_message = "I would like to know my account balance."
    response = chat_response(user_message)
    print(response)
