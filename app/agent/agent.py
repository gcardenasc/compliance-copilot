import json
import re
from app.services.llm import LLMService
from app.agent.tools import TOOL_SCHEMAS, execute_tool
from app.agent.prompts import SYSTEM_PROMPT

llm = LLMService()

def extract_json(text: str):
    if not text:
        return None
    
    try:
        # 1. Limpieza de bloques de código Markdown
        clean_text = re.sub(r'```json\s*|\s*```', '', text).strip()
        
        # 2. Encontrar el primer '{' y el último '}'
        start_idx = clean_text.find('{')
        end_idx = clean_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = clean_text[start_idx:end_idx+1]
            
            # 3. Intento de parseo directo
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # 4. Si falla, intentar una limpieza más agresiva de caracteres invisibles o saltos de línea mal formados
                json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str) 
                return json.loads(json_str)
                
    except Exception as e:
        print(f">>> Error crítico parseando JSON: {e}")
    
    return None

def run_agent(question: str, doc_id: str | None = None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Pregunta: {question}\n\nAnaliza el documento y responde solo en el formato JSON solicitado."}
    ]

    max_turns = 5
    cumulative_thoughts = ""
    used_tool_calls = set() # Sistema anti-bucle
    
    print(f"\n--- Iniciando Ciclo de Agente (Máx {max_turns} turnos) ---")

    for i in range(max_turns):
        print(f">>> Turno {i+1}...")
        try:
            response = llm.chat(messages, tools=TOOL_SCHEMAS)
        except Exception as e:
            return {"answer": f"Error de conexión con el LLM: {str(e)}", "citations": [], "confidence": 0}

        message = response.choices[0].message
        messages.append(message)

        # Capturar razonamiento textual del modelo
        if message.content:
            content_clean = re.sub(r'<think>.*?</think>', '', message.content, flags=re.DOTALL).strip()
            if content_clean and not extract_json(content_clean):
                cumulative_thoughts += f"🧠 **Pensamiento Turno {i+1}:**\n{content_clean}\n\n"

        # CASO A: El modelo quiere usar herramientas
        if message.tool_calls:
            for tool_call in message.tool_calls:
                t_name = tool_call.function.name
                t_args = tool_call.function.arguments
                
                # MECANISMO ANTI-BUCLE
                call_id = f"{t_name}-{t_args}"
                if call_id in used_tool_calls:
                    print(f"    [Aviso]: Bucle detectado. Forzando conclusión.")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": "Ya has llamado a esta herramienta con estos parámetros. No pidas más información redundante. Procede a dar tu respuesta final en JSON."
                    })
                    continue
                
                used_tool_calls.add(call_id)
                print(f"    [Herramienta]: {t_name} | Args: {t_args}")
                
                result = execute_tool(tool_call, doc_id)
                
                # LOG DETALLADO PARA DEBUG EN UI
                cumulative_thoughts += f"🔨 **Herramienta:** `{t_name}`\n"
                cumulative_thoughts += f"**Argumentos:** `{t_args}`\n"
                # Mostrar solo una parte del resultado para no saturar la UI
                preview = result[:1000] + "..." if len(result) > 1000 else result
                cumulative_thoughts += f"**Resultado:**\n{preview}\n\n"
                
                if len(result) > 4000:
                    result = result[:4000] + "\n... (truncado) ..."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            continue

        # CASO B: Respuesta final
        structured_data = extract_json(message.content) if message.content else None
        
        if structured_data:
            print(">>> Respuesta estructurada recibida.")
            if "thoughts" not in structured_data:
                structured_data["thoughts"] = cumulative_thoughts
            return structured_data
        
        if message.content and i >= 2:
            print("    [Aviso]: Fallo de formato JSON. Rescatando texto.")
            return {
                "answer": message.content,
                "citations": [],
                "confidence": 0.3,
                "thoughts": cumulative_thoughts + "\n⚠️ Nota: El modelo no generó JSON válido."
            }

    return {
        "answer": "Error: El agente no pudo consolidar una respuesta técnica tras varios intentos.",
        "citations": [],
        "confidence": 0,
        "thoughts": cumulative_thoughts
    }