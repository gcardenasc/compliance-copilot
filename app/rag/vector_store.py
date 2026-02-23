import chromadb
import uuid

client = chromadb.Client()
collection = client.get_or_create_collection("documents")


def add_documents(texts, embeddings, metadatas):

    ids = [str(uuid.uuid4()) for _ in texts]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def query_documents(query_embedding, n_results=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
