from app.rag.chunking import chunking_pipeline
from app.services.embeddings import embed_batch
from app.rag.vector_store import add_documents


def ingest_document(text: str, metadata=None):
    chunks = chunking_pipeline(text)
    embeddings = embed_batch(chunks)
    
    add_documents(
        texts=chunks,
        embeddings=embeddings,
        metadatas=[metadata] * len(chunks) if metadata else None
    )

    return len(chunks)
