from app.services.llm import LLMService
from app.agent.tools import TOOL_SCHEMAS, execute_tool
from app.agent.prompts import SYSTEM_PROMPT

llm = LLMService()

def run_agent(question: str, doc_id: str | None = None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    # Limit the number of turns to prevent infinite loops
    max_turns = 5
    
    for _ in range(max_turns):
        response = llm.chat(messages, tools=TOOL_SCHEMAS)
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            # If there's no tool call, it's the final answer
            return {"answer": message.content}

        # Process all tool calls in the message
        for tool_call in message.tool_calls:
            print(f">>> Ejecutando herramienta: {tool_call.function.name}")
            tool_result = execute_tool(tool_call, doc_id)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

    return {"answer": "Lo siento, he alcanzado el límite de interacciones sin llegar a una respuesta final."}