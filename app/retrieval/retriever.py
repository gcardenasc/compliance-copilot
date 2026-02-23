from app.services.embeddings import embed_query
from app.retrieval.vector_store import query_collection, get_by_metadata

def semantic_search(query: str, top_k=5):
    embedding = embed_query(query)
    results = query_collection(embedding, top_k=top_k)
    return results["documents"][0] if results["documents"] else []

def get_last_chunk(doc_id: str):
    results = get_by_metadata({"doc_id": doc_id} if doc_id else {})
    if not results["documents"]:
        return ""
        
    chunks = sorted(
        zip(results["documents"], results["metadatas"]),
        key=lambda x: x[1]["chunk_index"]
    )
    return chunks[-1][0] if chunks else ""

def get_chunk_by_index(doc_id: str, index: int):
    # Si tenemos ambos, necesitamos usar la sintaxis $and de ChromaDB
    if doc_id:
        query = {
            "$and": [
                {"doc_id": {"$eq": doc_id}},
                {"chunk_index": {"$eq": index}}
            ]
        }
    else:
        print(">>> ADVERTENCIA: No se proporcionó doc_id para get_chunk_by_index. Buscando globalmente.")
        query = {"chunk_index": {"$eq": index}}
        
    print(f">>> Buscando en ChromaDB: {query}")
    results = get_by_metadata(query)
    
    if results and results["documents"]:
        content = results["documents"][0]
        print(f">>> Resultado encontrado: {content[:50]}...")
        return content
    
    print(f">>> No se encontraron resultados para {query}")
    return "Error: No se encontró ningún párrafo con ese índice en el documento actual."