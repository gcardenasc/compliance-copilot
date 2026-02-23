import json
from app.retrieval.retriever import (
    semantic_search,
    get_chunk_by_index
)

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "semantic_search",
            "description": "Search semantically inside the document",
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
            "name": "get_chunk_by_index",
            "description": "Get a paragraph by its index",
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
        # Fallback if the model produces malformed JSON
        return "Error: Malformed tool call arguments."

    if name == "semantic_search":
        return "\n".join(semantic_search(args["query"], top_k=10))

    if name == "get_chunk_by_index":
        return get_chunk_by_index(doc_id, args["index"])

    return ""