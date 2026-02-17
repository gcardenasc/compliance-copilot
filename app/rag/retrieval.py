from app.services.embeddings import embed_text
from app.rag.vector_store import query

def retrieve_context(question: str, top_k=5):
    question_embedding = embed_text(question)
    results = query(question_embedding, top_k=top_k)
    docs = results.get("documents", [[]])[0]
    return "\n\n".join(docs)

def build_rag_prompt(question, context):
    rag_promt = f"""
    Usa SOLO la siguiente información para responder.
    Si no está en el contexto, di que no puedes responder.

    CONTEXTO:
    {context}

    PREGUNTA:
    {question}

    RESPUESTA:
    """
    print("CONTEXT:", context)
    return rag_promt