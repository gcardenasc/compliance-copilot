import os
from openai import OpenAI


client = OpenAI(
    base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
    api_key="lm-studio"
)

def generate_answer(prompt:str):
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "local-model"),
        messages=[
            {"role": "system", "content": "Eres un asistente experto en compliance."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content