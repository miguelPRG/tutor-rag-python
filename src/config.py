import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"
DATA_DIR = BASE_DIR / "data"
CHROMA_PATH = DATA_DIR / "chroma"

# Configurações de Modelos
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Garantir que pastas existem
DATA_DIR.mkdir(exist_ok=True)
CHROMA_PATH.mkdir(exist_ok=True)
