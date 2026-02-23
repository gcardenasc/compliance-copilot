from uuid import uuid4
from app.services.embeddings import embed_texts
from app.retrieval.vector_store import add_documents
from app.ingestion.parser import parse_document
from app.ingestion.chunking import chunk_text

def ingest_document(file_path):

    pages = parse_document(file_path)
    doc_id = str(uuid4())
    all_chunks = []
    chunk_index = 0

    print(f">>> Iniciando ingesta de {file_path.name}. Doc ID: {doc_id}")

    for page in pages:
        chunks = chunk_text(
            page["text"],
            page["page"],
            file_path.name
        )

        for chunk in chunks:
            chunk["metadata"]["doc_id"] = doc_id
            chunk["metadata"]["chunk_index"] = chunk_index
            chunk_index += 1

        all_chunks.extend(chunks)

    print(f">>> Total chunks generados: {len(all_chunks)}")

    texts = [c["text"] for c in all_chunks]
    metadatas = [c["metadata"] for c in all_chunks]
    
    # Debug: mostrar el primer metadato
    if metadatas:
        print(f">>> Ejemplo metadato chunk 0: {metadatas[0]}")

    embeddings = embed_texts(texts)

    add_documents(texts, embeddings, metadatas)

    return doc_id