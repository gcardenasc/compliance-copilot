from rank_bm25 import BM25Okapi
from app.services.embeddings import embed_query
from app.retrieval.vector_store import query_collection, get_by_metadata

# Caché simple en memoria para índices BM25 y corpus
_BM25_CACHE = {}

def get_bm25_index(doc_id: str):
    """Obtiene o crea el índice BM25 para un documento, usando caché."""
    if doc_id in _BM25_CACHE:
        return _BM25_CACHE[doc_id]["index"], _BM25_CACHE[doc_id]["data"]
    
    print(f">>> Construyendo índice BM25 para el documento: {doc_id}")
    all_chunks_data = get_by_metadata({"doc_id": doc_id} if doc_id else {})
    if not all_chunks_data or not all_chunks_data["documents"]:
        return None, None
    
    corpus = all_chunks_data["documents"]
    tokenized_corpus = [doc.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    
    # Guardar en caché
    _BM25_CACHE[doc_id] = {
        "index": bm25,
        "data": all_chunks_data
    }
    return bm25, all_chunks_data

def get_document_outline(doc_id: str):
    """Retorna una lista única de artículos y secciones detectadas para orientar al agente."""
    # Intentar usar el caché de BM25 si ya existe para evitar consulta pesada a DB
    if doc_id in _BM25_CACHE:
        results = _BM25_CACHE[doc_id]["data"]
    else:
        results = get_by_metadata({"doc_id": doc_id} if doc_id else {})
        
    if not results or not results["metadatas"]:
        return "No se detectó estructura en el documento."
    
    # Usamos diccionarios para mapear números a títulos y evitar duplicados
    articulos = {}
    capitulos = {}
    
    for meta in results["metadatas"]:
        art_num = meta.get("articulo")
        art_tit = meta.get("titulo")
        cap_num = meta.get("capitulo")
        cap_tit = meta.get("titulo_cap")
        
        if art_num:
            # Mantener el título si ya lo encontramos, o actualizar si este fragmento lo tiene
            if art_num not in articulos or (not articulos[art_num] and art_tit):
                articulos[art_num] = art_tit
        
        if cap_num:
            if cap_num not in capitulos or (not capitulos[cap_num] and cap_tit):
                capitulos[cap_num] = cap_tit
    
    output = []
    
    # Formatear Capítulos
    if capitulos:
        output.append("--- CAPÍTULOS ---")
        for num in sorted(capitulos.keys()):
            tit = capitulos[num]
            output.append(f"Capítulo {num}{': ' + tit if tit else ''}")
            
    # Formatear Artículos
    if articulos:
        output.append("\n--- ARTÍCULOS ---")
        # Intentar ordenar numéricamente si es posible
        try:
            sorted_arts = sorted(articulos.keys(), key=lambda x: int(re.sub(r'\D', '', x)))
        except:
            sorted_arts = sorted(articulos.keys())
            
        for num in sorted_arts:
            tit = articulos[num]
            output.append(f"Art. {num}{': ' + tit if tit else ''}")
    
    return "\n".join(output) if output else "Documento sin artículos numerados."

def rrf(vector_results, bm25_results, k=60):
    """Reciprocal Rank Fusion para combinar resultados de búsqueda vectorial y BM25."""
    scores = {}
    data_map = {}
    
    for rank, res in enumerate(vector_results):
        key = (res["index"], res["content"][:50])
        scores[key] = scores.get(key, 0) + 1 / (rank + k)
        data_map[key] = res

    for rank, res in enumerate(bm25_results):
        key = (res["index"], res["content"][:50])
        scores[key] = scores.get(key, 0) + 1 / (rank + k)
        if key not in data_map:
            data_map[key] = res

    sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    return [data_map[k] for k in sorted_keys]

def semantic_search(query: str, doc_id: str = None, top_k=5):
    """Búsqueda Híbrida optimizada con inyección de página en el texto."""
    
    # 1. Búsqueda Vectorial (Dense)
    embedding = embed_query(query)
    where = {"doc_id": doc_id} if doc_id else None
    vector_raw = query_collection(embedding, top_k=top_k*2, where=where)
    
    vector_results = []
    if vector_raw and vector_raw["documents"]:
        for doc, meta in zip(vector_raw["documents"][0], vector_raw["metadatas"][0]):
            page_num = meta.get("page", "N/A")
            vector_results.append({
                # Inyectamos la página directamente en el contenido para que el LLM no la pierda
                "content": f"[PÁGINA {page_num}] {doc}",
                "index": meta.get("chunk_index"),
                "page": page_num,
                "article": meta.get("articulo", "N/A"),
                "title": meta.get("titulo", ""),
                "source": "vector"
            })
    
    # 2. Búsqueda BM25 (Sparse) con Caché
    bm25, all_chunks_data = get_bm25_index(doc_id)
    if not bm25:
        return vector_results[:top_k]
    
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    
    top_n_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k*2]
    
    bm25_results = []
    for i in top_n_indices:
        if bm25_scores[i] <= 0: continue
        meta = all_chunks_data["metadatas"][i]
        page_num = meta.get("page", "N/A")
        bm25_results.append({
            "content": f"[PÁGINA {page_num}] {all_chunks_data['documents'][i]}",
            "index": meta.get("chunk_index"),
            "page": page_num,
            "article": meta.get("articulo", "N/A"),
            "title": meta.get("titulo", ""),
            "source": "bm25"
        })

    # 3. Fusión RRF
    hybrid_results = rrf(vector_results, bm25_results)
    return hybrid_results[:top_k]

def search_by_metadata(doc_id: str, field: str, value: str):
    """Busca fragmentos que coincidan exactamente con un metadato (ej. articulo='30')"""
    query = {
        "$and": [
            {"doc_id": {"$eq": doc_id}},
            {field: {"$eq": value}}
        ]
    }
    results = get_by_metadata(query)
    if results and results["documents"]:
        return [{"content": d, "index": m.get("chunk_index"), "page": m.get("page"), "title": m.get("titulo", "")} 
                for d, m in zip(results["documents"], results["metadatas"])]
    return []

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
    if doc_id:
        query = {
            "$and": [
                {"doc_id": {"$eq": doc_id}},
                {"chunk_index": {"$eq": index}}
            ]
        }
    else:
        query = {"chunk_index": {"$eq": index}}
        
    results = get_by_metadata(query)
    if results and results["documents"]:
        return results["documents"][0]
    return "Error: No se encontró ningún párrafo con ese índice."