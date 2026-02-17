import os
from openai import OpenAI

# LM Studio OpenAI-compatible endpoint
client = OpenAI(
    base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
    api_key="lm-studio"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-nomic-embed-text-v1.5"
)


def embed_text(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def embed_batch(texts: list[str]):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]

# def embed_batch(texts: list[str]):
#     return [embed_text(t) for t in texts]