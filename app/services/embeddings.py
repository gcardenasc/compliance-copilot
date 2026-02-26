import os
import time
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
EMBEDDING_MODEL = "BAAI/bge-m3"

# Cliente oficial de HuggingFace
client = InferenceClient(token=HF_TOKEN)

def get_embeddings(inputs):
    """Llamada robusta usando el cliente oficial para feature-extraction."""
    max_retries = 3
    for i in range(max_retries):
        try:
            # Forzamos explícitamente la tarea de extracción de características (embeddings)
            response = client.feature_extraction(
                text=inputs,
                model=EMBEDDING_MODEL
            )
            # El cliente devuelve un ndarray o lista dependiendo de la entrada
            return response.tolist() if hasattr(response, 'tolist') else response
        except Exception as e:
            error_str = str(e)
            if "estimated_time" in error_str or "loading" in error_str.lower():
                print(f">>> Modelo BGE-M3 cargándose. Reintento {i+1}/{max_retries}...")
                time.sleep(20)
                continue
            raise ValueError(f"HuggingFace Error: {error_str}")
            
    raise ValueError("HuggingFace API timeout: Model failed to load.")

def embed_texts(texts: list[str]):
    return get_embeddings(texts)

def embed_query(query: str):
    result = get_embeddings([query])
    # Si la respuesta es una lista de listas (lote), tomamos la primera
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
        return result[0]
    return result