from langchain_chroma import Chroma
from embeddings import get_embeddings   # ← Important: no 'src.'
import os
import shutil

def create_vectorstore(docs):
    """Create new vector store from documents"""
    if not docs:
        print("⚠️ No documents to index.")
        return None
    
    embeddings = get_embeddings()
    
    # Clear old database if exists
    if os.path.exists("chroma_db"):
        import shutil
        shutil.rmtree("chroma_db")
    
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="chroma_db",
        collection_name="rag_docs"
    )
    print("✅ Vector store created successfully!")
    return vectorstore

def get_vectorstore():
    """Load existing vector store"""
    embeddings = get_embeddings()
    
    if not os.path.exists("chroma_db"):
        print("⚠️ No existing vector store found. Please process documents first.")
        return None
    
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings,
        collection_name="rag_docs"
    )