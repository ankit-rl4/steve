import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from config import ENDPOINT, KEYAPI

# Fetch endpoint and deployment name from environment variables or config
endpoint = os.getenv("ENDPOINT_URL", ENDPOINT)
deployment = os.getenv("DEPLOYMENT_NAME", "steve01-gpt4")

# Create a token provider using DefaultAzureCredential
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

# Initialize AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

def chat_response(user_message):
    # Create chat completion request
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a customer service representative from Bank of Baroda. Please reply to customer requests using polite and respectful language."},
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
