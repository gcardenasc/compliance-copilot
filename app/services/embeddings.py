import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
# Modelo multilingüe potente
EMBEDDING_MODEL = "BAAI/bge-m3"
API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMBEDDING_MODEL}"

def embed_texts(texts: list[str]):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    return response.json()

def embed_query(query: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": [query], "options": {"wait_for_model": True}})
    # Retornamos el primer (y único) embedding
    return response.json()[0]