from langchain_ollama import OllamaEmbeddings

def get_embeddings():
    """Return embeddings model"""
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )