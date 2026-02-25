import re


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_metadata_from_line(line: str):
    """Detecta si una línea es el inicio de un artículo o capítulo."""
    # Soporta "Artículo 5", "Art. 5", "(5)"
    art_match = re.search(r"^(?:Art[ií]culo|Art\.?)\s*(\d+)", line, re.I)
    if not art_match:
        art_match = re.search(r"^\s*\((\d+)\)", line)
    
    if art_match:
        num = str(int(art_match.group(1)))
        title = line[art_match.end():].strip().strip('.: ')
        return {"articulo": num, "titulo": title if len(title) < 120 else None}
        
    cap_match = re.search(r"^Cap[ií]tulo\s+([A-Z0-9]+)", line, re.I)
    if cap_match:
        num = cap_match.group(1)
        title = line[cap_match.end():].strip().strip('.: ')
        return {"capitulo": num, "titulo_cap": title if len(title) < 150 else None}
        
    return None


def chunk_text(text: str, page: int, source: str):
    """Segmenta el texto de forma inteligente detectando cambios de artículo."""
    lines = text.split("\n")
    chunks = []
    
    current_text = []
    current_meta = {
        "articulo": None,
        "titulo": None,
        "capitulo": None
    }
    
    chunk_index = 0

    for line in lines:
        line_clean = line.strip()
        if not line_clean: continue
        
        new_meta = extract_metadata_from_line(line_clean)
        
        # Si detectamos un nuevo artículo/capítulo, cerramos el chunk actual y empezamos uno nuevo
        if new_meta and (new_meta.get("articulo") or new_meta.get("capitulo")):
            if current_text:
                full_text = clean_text("\n".join(current_text))
                if full_text:
                    chunks.append({
                        "text": full_text,
                        "metadata": {
                            "page": page,
                            "source": source,
                            "paragraph_index": chunk_index,
                            **{k: v for k, v in current_meta.items() if v is not None}
                        }
                    })
                    chunk_index += 1
            
            # Resetear estado con la nueva información
            current_text = [line_clean]
            current_meta.update(new_meta)
            if "articulo" in new_meta:
                print(f"    [Ingesta] Detectado Art. {new_meta['articulo']} en pág {page}")
        else:
            current_text.append(line_clean)

    # Añadir el último fragmento
    if current_text:
        full_text = clean_text("\n".join(current_text))
        if full_text:
            chunks.append({
                "text": full_text,
                "metadata": {
                    "page": page,
                    "source": source,
                    "paragraph_index": chunk_index,
                    **{k: v for k, v in current_meta.items() if v is not None}
                }
            })

    return chunks
