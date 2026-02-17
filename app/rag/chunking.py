import re

STRUCTURE_PATTERN = (
    r"(Art\.?\s*\d+|Artículo\s+\d+|"
    r"Cap[ií]tulo\s+\w+|Sección\s+\w+|"
    r"\d+\.\s+[A-Z].+|"           
    r"Annex\s+[A-Z]|Appendix\s+[A-Z])"
)


def clean_text(text: str) -> str:
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_by_structure(text: str):
    parts = re.split(STRUCTURE_PATTERN, text, flags=re.IGNORECASE)

    if len(parts) < 3:
        return []

    chunks = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        chunks.append(f"{header}\n{body}".strip())

    return chunks


def chunk_by_length(text: str, size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += size - overlap

    return chunks


def chunking_pipeline(text: str):
    text = clean_text(text)

    structured_chunks = split_by_structure(text)

    if not structured_chunks:
        return chunk_by_length(text)

    final_chunks = []

    for chunk in structured_chunks:
        if len(chunk) > 1200:
            final_chunks.extend(chunk_by_length(chunk))
        else:
            final_chunks.append(chunk)

    return final_chunks
