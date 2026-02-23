import re


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_metadata_from_chunk(chunk: str):
    metadata = {}

    articulo = re.search(r"\((\d+)\)", chunk)
    if articulo:
        metadata["articulo"] = articulo.group(1)

    capitulo = re.search(r"Cap[ií]tulo\s+([A-Z0-9]+)", chunk, re.I)
    if capitulo:
        metadata["capitulo"] = capitulo.group(1)

    seccion = re.search(r"Secci[oó]n\s+([A-Z0-9]+)", chunk, re.I)
    if seccion:
        metadata["seccion"] = seccion.group(1)

    return metadata


def split_large_paragraph(paragraph, max_chars=800):
    words = paragraph.split()
    chunks = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            chunks.append(current.strip())
            current = word
        else:
            current += " " + word

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_text(text: str, page: int, source: str):
    paragraphs = text.split("\n\n")
    chunks = []

    for i, p in enumerate(paragraphs):
        chunks.append({
            "text": p,
            "metadata": {
                "page": page,
                "source": source,
                "paragraph_index": i
            }
        })

    return chunks
