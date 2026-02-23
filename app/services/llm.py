from openai import OpenAI

class LLMService:

    def __init__(self, model="deepseek/deepseek-r1-0528-qwen3-8b"):
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"  # puede ser cualquier string
        )
        self.model = model

    def chat(self, messages, tools=None, tool_choice="auto"):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice
        )