import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")

class ComplianceAPIClient:
    def __init__(self):
        self.base_url = BASE_URL

    def get_documents(self):
        # Asumiendo un endpoint que liste archivos procesados
        try:
            response = requests.get(f"{self.base_url}/documents")
            return response.json() if response.status_code == 200 else []
        except:
            return []

    def upload_file(self, file):
        files = {"file": (file.name, file.getvalue())}
        response = requests.post(f"{self.base_url}/upload", files=files)
        return response.json()

    def ask_question(self, question: str, doc_id: str, strict_mode: bool = False):
        payload = {
            "question": question,
            "doc_id": doc_id,
            "config": {"strict": strict_mode}
        }
        response = requests.post(f"{self.base_url}/qa", json=payload)
        return response.json()
