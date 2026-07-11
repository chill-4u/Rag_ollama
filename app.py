import streamlit as st
import os
import sys

# Aggressive path fix
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.getcwd())

print(f"Current directory: {current_dir}")  # For debugging

# Imports
from loader import load_and_split_documents
from vectorestore import create_vectorstore
from rag import create_rag_chain

st.set_page_config(page_title="RAG Document Q&A", page_icon="📚", layout="wide")

st.title("📚 RAG Document Question & Answer System")
st.markdown("**Upload PDFs → Ask questions about them**")

# Sidebar
with st.sidebar:
    st.header("📁 Document Management")
    
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])
    
    if st.button("🔄 Process Documents", type="primary"):
        if uploaded_files:
            if not os.path.exists("data"):
                os.makedirs("data")
            
            for file in uploaded_files:
                with open(f"data/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
            
            with st.spinner("Processing documents..."):
                splits = load_and_split_documents()
                if splits:
                    create_vectorstore(splits)
                    st.success(f"✅ Processed {len(uploaded_files)} document(s)!")
                else:
                    st.error("No documents found.")
        else:
            st.warning("Upload PDFs first!")

    if st.button("🗑️ Clear Database"):
        if os.path.exists("chroma_db"):
            import shutil
            shutil.rmtree("chroma_db")
            st.success("Database cleared!")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chain = create_rag_chain()
            response = chain.invoke(question) if chain else "Please process documents first!"
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})