import chromadb
import uuid
from pathlib import Path

# Use a persistent client
db_path = Path("data/chroma")
db_path.mkdir(parents=True, exist_ok=True)
client = chromadb.PersistentClient(path=str(db_path))
collection = client.get_or_create_collection("documents")

# Log del estado inicial
print(f">>> ChromaDB inicializado. Documentos en colección: {collection.count()}")

def add_documents(documents, embeddings, metadatas):
    # Generar IDs únicos para evitar colisiones entre diferentes cargas
    ids = [str(uuid.uuid4()) for _ in documents]
    
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(embedding, top_k=5, where=None):
    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=where
    )

def get_by_metadata(where: dict):
    return collection.get(where=where)