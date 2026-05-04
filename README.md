# Tutor RAG para Programação Python

Este é um MVP de um chatbot educacional que utiliza **Retrieval-Augmented Generation (RAG)** para ajudar estudantes iniciantes na linguagem Python.

## Objetivo
O objetivo é fornecer respostas pedagógicas que não entreguem a solução de imediato, mas que guiem o estudante através de explicações passo-a-passo e perguntas orientadoras, baseando-se num corpus de conhecimento local.

## Estrutura do Projeto
- `corpus/`: Ficheiros Markdown com o conteúdo educativo.
- `src/`: Código fonte (ingestão, pesquisa, geração e interface).
- `data/`: Local de armazenamento da base de dados vetorial ChromaDB.

## Requisitos
- Python 3.11 ou superior.
- Gestor de pacotes `uv` (recomendado).
- Chave de API do Google Gemini (Desativado: agora usa Ollama).
- Ollama instalado e a correr localmente com o modelo `llama3.2`.

## Instalação

1. **Instalar o `uv`** (se ainda não tiver):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Sincronizar dependências**:
   ```bash
   uv sync
   ```

3. **Configurar variáveis de ambiente**:
   Crie um ficheiro `.env` a partir do exemplo:
   ```bash
   cp .env.example .env
   ```
   Certifique-se de que o Ollama está acessível no HOST configurado no `.env`.

## Como Executar

1. **Garantir que o Ollama tem o modelo**:
   ```bash
   ollama pull llama3.2
   ```

2. **Indexar o corpus** (necessário na primeira execução):
   ```bash
   uv run python src/ingest.py
   ```

2. **Correr a aplicação Streamlit**:
   ```bash
   uv run streamlit run src/app.py
   ```

## Stack Técnica
- **Streamlit**: Interface web.
- **ChromaDB**: Base de dados vetorial.
- **Sentence-Transformers**: Embeddings locais (`all-MiniLM-L6-v2`).
- **Ollama**: Modelo de linguagem local (`llama3.2`).
- **uv**: Gestão de pacotes e ambiente virtual.
