import os
import time
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
# Modelo multilingüe optimizado por defecto
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Cliente oficial de HuggingFace
client = InferenceClient(token=HF_TOKEN)

# Caché simple en memoria
_EMBEDDING_CACHE = {}

def get_embeddings(inputs):
    """Llamada robusta usando el cliente oficial para feature-extraction con caché."""
    # Revisar caché para entradas individuales
    if isinstance(inputs, str):
        if inputs in _EMBEDDING_CACHE:
            return _EMBEDDING_CACHE[inputs]
    elif isinstance(inputs, list) and len(inputs) == 1:
        if inputs[0] in _EMBEDDING_CACHE:
            return [_EMBEDDING_CACHE[inputs[0]]]

    max_retries = 3
    for i in range(max_retries):
        try:
            response = client.feature_extraction(
                text=inputs,
                model=EMBEDDING_MODEL
            )
            result = response.tolist() if hasattr(response, 'tolist') else response
            
            # Guardar en caché
            if isinstance(inputs, str):
                _EMBEDDING_CACHE[inputs] = result
            elif isinstance(inputs, list) and len(inputs) == 1:
                _EMBEDDING_CACHE[inputs[0]] = result[0]
                
            return result
        except Exception as e:
            error_str = str(e)
            if "estimated_time" in error_str or "loading" in error_str.lower():
                print(f">>> Modelo {EMBEDDING_MODEL} cargándose. Reintento {i+1}/{max_retries}...")
                time.sleep(20)
                continue
            raise ValueError(f"HuggingFace Error: {error_str}")
            
    raise ValueError(f"HuggingFace API timeout: Model {EMBEDDING_MODEL} failed to load.")

def embed_texts(texts: list[str]):
    return get_embeddings(texts)

def embed_query(query: str):
    result = get_embeddings([query])
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
        return result[0]
    return result