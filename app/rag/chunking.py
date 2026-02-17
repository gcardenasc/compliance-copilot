import re

SPLIT_PATTERN = r"(Artículo\s+\d+|Sección\s+\d+|Capítulo\s+\w+)"

def clean_text(text):
    return " ".join(text.split())

def split_by_structure(text):
    parts = re.split(SPLIT_PATTERN, text)

    chunks = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        chunks.append(header + " " + body)
    return chunks

def chunk_by_length(text, size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap

    return chunks

def chunking_pipeline(text):
    text = clean_text(text)

    structured = split_by_structure(text)

    final_chunks = []
    for chunk in structured:
        if len(chunk) > 1000:
            final_chunks.extend(chunk_by_length(chunk))
        else:
            final_chunks.append(chunk)

    return final_chunks