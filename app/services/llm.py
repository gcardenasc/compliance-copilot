import os
from openai import OpenAI

class LLMService:

    def __init__(self, model=None):
        # Prioridad: argumento -> variable de entorno -> valor por defecto
        self.model = model or os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        
        # Usamos la API de Groq Cloud
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def chat(self, messages, tools=None, tool_choice="auto"):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0.0
        )