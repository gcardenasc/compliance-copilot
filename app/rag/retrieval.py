from app.services.embeddings import embed_text
from app.rag.vector_store import query_documents


def retrieve_context(question: str, top_k=5):
    question_embedding = embed_text(question)

    results = query_documents(question_embedding, n_results=top_k)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    context_parts = []

    for doc, meta in zip(docs, metas):
        citation = ""

        if meta:
            page = meta.get("page")
            source = meta.get("source")

            if source:
                citation += f"[{source}"
                if page:
                    citation += f" - pág. {page}"
                citation += "]"

        context_parts.append(f"{doc}\n{citation}")

    return "\n\n".join(context_parts)


def build_rag_prompt(question, context):
    return f"""
Usa SOLO la siguiente información para responder.
Si la respuesta no está explícitamente en el contexto, di:
"No puedo responder con la información disponible."

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
"""
