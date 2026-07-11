from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from reteriever import get_retriever

def create_rag_chain():
    """Create the complete RAG chain"""
    retriever = get_retriever(k=4)
    if retriever is None:
        return None
    
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.3,
        num_ctx=8192,
        base_url="http://localhost:11434"
    )
    
    template = """You are a helpful assistant. Answer the question based **only** on the following context.
If you don't know the answer, say "I don't have enough information in the documents to answer this."

Context:
{context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain