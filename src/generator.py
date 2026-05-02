import ollama
from config import OLLAMA_MODEL_NAME, OLLAMA_HOST
from prompts import SYSTEM_PROMPT

class Generator:
    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.model = OLLAMA_MODEL_NAME

    def generate_response(self, question: str, context: str):
        """Gera uma resposta pedagógica usando o Ollama."""
        prompt = SYSTEM_PROMPT.format(question=question, context=context)
        
        try:
            response = self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Lamento, ocorreu um erro ao contactar o tutor (Ollama): {str(e)}. Garante que o Ollama está a correr e que tens o modelo {self.model} instalado."
