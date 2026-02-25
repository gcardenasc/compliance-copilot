import json
from app.retrieval.retriever import (
    semantic_search,
    get_chunk_by_index,
    search_by_metadata,
    get_document_outline
)

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_document_outline",
            "description": "Returns a list of all detected articles and sections in the document. Use this at the beginning to orient yourself.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "semantic_search",
            "description": "Search semantically inside the document. Returns text chunks with their indices and metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_by_article",
            "description": "Find chunks for a specific article number (e.g., '30'). Use this if semantic search fails or you have an article reference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "string"}
                },
                "required": ["number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_chunk_by_index",
            "description": "Get a paragraph by its index. Use this to explore surrounding context after a search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"}
                },
                "required": ["index"]
            }
        }
    }
]

def execute_tool(tool_call, doc_id=None):

    name = tool_call.function.name
    try:
        args = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return "Error: Malformed tool call arguments."

    if name == "get_document_outline":
        return get_document_outline(doc_id)

    if name == "semantic_search":
        results = semantic_search(args["query"], doc_id=doc_id, top_k=10)
        return json.dumps(results, indent=2, ensure_ascii=False)

    if name == "search_by_article":
        results = search_by_metadata(doc_id, "articulo", args["number"])
        return json.dumps(results, indent=2, ensure_ascii=False)

    if name == "get_chunk_by_index":
        return get_chunk_by_index(doc_id, args["index"])

    return ""