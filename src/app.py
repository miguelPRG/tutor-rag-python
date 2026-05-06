import streamlit as st
from retriever import Retriever
from generator import Generator
from ingest import ingest_documents
from config import CHROMA_PATH, OLLAMA_MODEL_NAME

# Configuração da página
st.set_page_config(page_title="Tutor RAG Python", page_icon="🐍", layout="wide")

# Indexar corpus automaticamente ao iniciar
@st.cache_resource
def initialize_corpus():
    """Verifica e indexa o corpus se necessário."""
    chroma_db_file = CHROMA_PATH / "chroma.sqlite3"
    if not chroma_db_file.exists():
        with st.spinner("📚 A indexar corpus pela primeira vez..."):
            ingest_documents()
    return True

# Executar inicialização
initialize_corpus()

# Estilos CSS Customizados para o tema Frosted Glass
st.markdown("""
<style>
    /* Estilo Base e Fundo */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Mensagens do Chat */
    .message-bot {
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        padding: 1rem;
        border-radius: 0.5rem 1rem 1rem 0.5rem;
        margin-bottom: 1rem;
    }
    
    .message-user {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 1rem 0.5rem 0.5rem 1rem;
        margin-bottom: 1rem;
        text-align: right;
    }

    /* Texto e Cabeçalhos */
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
    
    .python-accent {
        color: #38bdf8;
        font-weight: bold;
    }

    /* Esconder o estilo padrão do Streamlit em alguns pontos */
    /* .stChatInputContainer {
        border-top: none !important;
        background: transparent !important;
    } */
    
    /* .stChatInput {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0.75rem !important;
    } */
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Aplicação
st.markdown(f"""
<div class="glass-card" style="margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="width: 40px; height: 40px; background: #0ea5e9; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">P</div>
        <div>
            <h1 style="margin: 0; font-size: 24px;">Tutor RAG Python</h1>
            <p style="margin: 0; font-size: 14px; opacity: 0.7;">Assistente Pedagógico • Modelo {OLLAMA_MODEL_NAME}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div class="glass-card">
        <h3>Sistema</h3>
        <p style="font-size: 14px;">Local: ChromaDB ✅</p>
        <p style="font-size: 14px;">LLM: Ollama ({OLLAMA_MODEL_NAME}) ✅</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Re-indexar Corpus Local"):
        with st.status("A processar documentos...", expanded=True) as status:
            status.update(label="A indexar documentos no ChromaDB...", state="running")
            ingest_documents()
            status.update(label="Indexação completa!", state="complete", expanded=False)
        st.success("Documentos prontos para consulta.")

# Área de Chat
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role_class = "message-bot" if message["role"] == "assistant" else "message-user"
        prefix = "🤖 Tutor:" if message["role"] == "assistant" else "👤 Tu:"
        st.markdown(f"""
        <div class="{role_class}">
            <div style="font-size: 12px; font-weight: bold; margin-bottom: 5px; opacity: 0.8;">{prefix}</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Diz-me, em que parte do Python estás com dúvidas?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Lógica de Geração (executa apenas após o rerun do input para manter ordem)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        try:
            # 1. Recuperar Contexto
            retriever = Retriever()
            context, sources = retriever.get_context(last_prompt)
            
            # 2. Gerar Resposta
            generator = Generator()
            response = generator.generate_response(last_prompt, context)
            
            # 3. Mostrar Resposta com as fontes se existirem
            full_response = response
            if sources:
                full_response += f"\n\n---\n*Fontes consultadas: {', '.join(sources)}*"
            
            st.markdown(full_response)
            
            # Guardar no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun() 
            
        except Exception as e:
            st.error(f"Ocorreu um erro na comunicação local: {e}. Garante que o Ollama está ativo.")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; opacity: 0.5; font-size: 10px;">
    MVP Python Tutor RAG • uv • streamlit • chromadb • ollama
</div>
""", unsafe_allow_html=True)
