import chromadb
from sentence_transformers import SentenceTransformer
from config import CORPUS_DIR, CHROMA_PATH, EMBEDDING_MODEL_NAME

def ingest_documents():
    """Lê documentos md, cria embeddings e guarda no ChromaDB."""
    # Inicializar modelo de embeddings
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    # Inicializar ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name="python_tutor")
    
    # Listar ficheiros
    files = list(CORPUS_DIR.glob("*.md"))
    
    documents = []
    metadatas = []
    ids = []
    
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Divisão simples por títulos (Markdown) ou parágrafos duplos
        chunks = content.split("\n\n")
        
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
                
            chunk_id = f"{file.name}_{i}"
            documents.append(chunk)
            metadatas.append({"source": file.name, "chunk": i})
            ids.append(chunk_id)
            
    if documents:
        # Gerar embeddings
        embeddings = model.encode(documents).tolist()
        
        # Adicionar ou atualizar à coleção (upsert evita erro de IDs duplicados)
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Indexados {len(documents)} blocos de {len(files)} ficheiros.")
    else:
        print("Nenhum documento encontrado para indexar.")

if __name__ == "__main__":
    ingest_documents()
