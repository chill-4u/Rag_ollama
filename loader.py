from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_and_split_documents():
    """Load PDFs from data/ folder and split into chunks"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created 'data/' folder. Please add PDF files there.")
        return []
    
    loader = PyPDFDirectoryLoader("data/")
    documents = loader.load()
    
    if not documents:
        print("⚠️ No PDF documents found in 'data/' folder.")
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"✅ Loaded {len(documents)} documents and created {len(splits)} chunks.")
    return splits