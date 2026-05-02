import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, EMBEDDING_MODEL_NAME

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(name="python_tutor")

    def get_context(self, question: str, n_results: int = 3):
        """Pesquisa documentos relevantes para a pergunta."""
        try:
            # Verificar se a coleção tem dados
            if self.collection.count() == 0:
                return "", []

            # Gerar embedding da pergunta
            query_embedding = self.model.encode([question]).tolist()
            
            # Pesquisar
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            context = "\n---\n".join(results['documents'][0])
            sources = [meta['source'] for meta in results['metadatas'][0]]
            
            return context, list(set(sources))
        except Exception as e:
            print(f"Erro no retriever: {e}")
            return "", []
