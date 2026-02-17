import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./data/chroma"))

collection = client.get_or_create_collection(name="documents")

def add_documents(texts, embeddings, metadatas=None):
    ids = [str(i) for i in range(len(texts))]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results