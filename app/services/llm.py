import os
from openai import OpenAI

class LLMService:

    def __init__(self, model="meta-llama-3.1-8b-instruct"):
        # Usamos variable de entorno para la URL, útil para Docker
        base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        self.client = OpenAI(
            base_url=base_url,
            api_key="lm-studio"
        )
        self.model = model

    def chat(self, messages, tools=None, tool_choice="auto"):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0.0
        )