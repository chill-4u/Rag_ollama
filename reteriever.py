from vectorestore import get_vectorstore

def get_retriever(k=4):
    """Return document retriever"""
    vectorstore = get_vectorstore()
    if vectorstore is None:
        return None
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )