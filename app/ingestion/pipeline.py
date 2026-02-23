from app.rag.chunking import chunking_pipeline
from app.services.embeddings import embed_batch
from app.rag.vector_store import add_documents


def ingest_document(text: str, metadata: dict | None = None):

    print(">>> TEXTO RECIBIDO:", len(text))

    chunk_dicts = chunking_pipeline(text)
    print(">>> CHUNKS GENERADOS:", len(chunk_dicts))

    texts = []
    metadatas = []

    for chunk in chunk_dicts:
        chunk_text = chunk["text"]
        chunk_metadata = chunk.get("metadata", {}).copy()

        # Merge metadata global si existe
        if metadata:
            chunk_metadata = {**chunk_metadata, **metadata}

        texts.append(chunk_text)
        metadatas.append(chunk_metadata)

    # Seguridad estructural
    assert len(texts) == len(metadatas)

    embeddings = embed_batch(texts)
    print(">>> EMBEDDINGS GENERADOS:", len(embeddings))

    add_documents(
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(texts)
