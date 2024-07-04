import openai
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

retriever_model = SentenceTransformer('all-MiniLM-L6-v2')

df = pd.read_csv('marketing_database.csv')

corpus = df['product_description'].tolist()
corpus_embeddings = retriever_model.encode(corpus, convert_to_tensor=True)


def retrieve_relevant_info(query, top_k=3):
    query_embedding = retriever_model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    relevant_docs = [corpus[hit['corpus_id']] for hit in hits[0]]
    return relevant_docs

def generate_marketing_content(customer_info, relevant_info):
    prompt = f"Create an SMS marketing message for the following customer info and product details:\n\nCustomer Info: {customer_info}\n\nProduct Details:\n"
    for info in relevant_info:
        prompt += f"- {info}\n"
    prompt += "\nMessage:"

    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=50
    )

    return response.choices[0].text.strip()

customer_info = "Customer: John Doe, Interests: Home improvement, Age: 35"
query = "home improvement tools"
relevant_info = retrieve_relevant_info(query)

sms_message = generate_marketing_content(customer_info, relevant_info)
print(sms_message)
