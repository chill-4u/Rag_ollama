# 📚 RAG Document Question & Answer System

A powerful **Retrieval-Augmented Generation (RAG)** application that lets you upload PDF documents and ask intelligent questions about them. Built with LangChain, Ollama, and Streamlit.

## 🌟 Features

- **📄 Multi-PDF Support**: Upload and process multiple PDF documents simultaneously
- **🔍 Intelligent Retrieval**: Semantic search using embeddings to find relevant document chunks
- **💬 Interactive Q&A**: Ask natural language questions and get accurate answers based on your documents
- **🚀 Local LLM**: Run everything locally using Ollama (no API keys needed)
- **💾 Persistent Storage**: Vector database stores embeddings for quick retrieval
- **🧹 Easy Management**: Clear database and reprocess documents with one click

## 🔧 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Ollama** installed and running locally ([Download here](https://ollama.ai))
- **Git** (optional, for cloning)

### Required Ollama Models

This project requires two Ollama models. Download them using:

```bash
ollama pull nomic-embed-text  # For embeddings
ollama pull llama3.2          # For LLM responses
```

Verify Ollama is running:
```bash
# Ollama should be accessible at http://localhost:11434
curl http://localhost:11434/api/tags
```

## 📦 Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd Rag_project
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Required Folders

```bash
mkdir data
mkdir chroma_db
```

## 🚀 Quick Start

### 1. Start Ollama

Make sure Ollama is running in the background:

```bash
ollama serve
```

(Or if you installed Ollama as a service, it runs automatically)

### 2. Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Upload and Process Documents

1. Click **"Upload PDF files"** in the sidebar
2. Select one or more PDF files
3. Click **"🔄 Process Documents"**
4. Wait for the success message

### 4. Ask Questions

Type your question in the chat box and press Enter. The system will:
- Search your documents for relevant content
- Use the LLM to generate an accurate answer
- Display the response in the chat

## 📁 Project Structure

```
Rag_project/
├── data/                    # Folder for uploaded PDFs
├── chroma_db/              # Vector store (auto-created)
├── __init__.py             # Package initialization
├── app.py                  # Streamlit UI & main app
├── loader.py               # PDF loading & chunking
├── embeddings.py           # Embedding model setup
├── vectorstore.py          # ChromaDB operations
├── retriever.py            # Document retriever
├── rag.py                  # RAG chain assembly
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (optional)
└── README.md              # This file
```

## 🔄 How It Works

### Architecture Flow

```
User Query
    ↓
[RAG Chain]
    ├── Retriever: Find similar documents using embeddings
    ├── Formatter: Prepare context from retrieved docs
    ├── Prompt Template: Build structured prompt
    ├── LLM (Ollama): Generate answer based on context
    └── Output Parser: Return clean response
    ↓
User sees Answer
```

### Detailed Process

1. **Document Upload & Loading** (`loader.py`)
   - PDFs are loaded using `PyPDFDirectoryLoader`
   - Split into chunks (1000 characters, 200 char overlap)

2. **Embeddings** (`embeddings.py`)
   - Uses `nomic-embed-text` model from Ollama
   - Converts text chunks into vector embeddings

3. **Vector Store** (`vectorstore.py`)
   - Stores embeddings in ChromaDB
   - Enables semantic similarity search
   - Persists data in `chroma_db/` folder

4. **Retrieval** (`retriever.py`)
   - Searches for 4 most similar documents by default
   - Returns relevant chunks for context

5. **RAG Chain** (`rag.py`)
   - Combines retrieved documents as context
   - Sends to `llama3.2` model with your question
   - Returns grounded, factual answers

## ⚙️ Configuration

### Modify Chunk Settings

Edit `loader.py` to adjust document chunking:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Increase for longer contexts
    chunk_overlap=200,      # Increase for more overlap
    ...
)
```

### Adjust Retrieval Count

Edit `retriever.py` to retrieve more/fewer documents:

```python
search_kwargs={"k": 4}  # Change 4 to desired number
```

### Change LLM Temperature

Edit `rag.py` to adjust creativity vs. accuracy:

```python
llm = ChatOllama(
    model="llama3.2",
    temperature=0.3,  # 0.0 = deterministic, 1.0 = creative
    ...
)
```

## 🔍 Troubleshooting

### ❌ "Failed to connect to Ollama"

**Solution**: Make sure Ollama is running
```bash
ollama serve
# Check if accessible:
curl http://localhost:11434/api/tags
```

### ❌ "No PDF documents found in 'data/' folder"

**Solution**: Ensure PDFs are in the `data/` folder:
```bash
# Create data folder if missing
mkdir data
# Add PDFs to it
```

### ❌ "No existing vector store found"

**Solution**: Process documents first
1. Upload PDFs in the sidebar
2. Click "🔄 Process Documents"
3. Then ask questions

### ❌ Application crashes or hangs

**Solution**: 
- Increase available RAM (larger documents need more memory)
- Reduce `chunk_size` in `loader.py`
- Use smaller PDFs for testing
- Check Ollama logs for errors

### ⚠️ Slow responses

**Solution**:
- Ensure Ollama has enough VRAM/RAM
- Reduce number of retrieved documents (k parameter)
- Use smaller model if available
- Check system resources: `top` or Task Manager

## 📊 Usage Examples

### Example 1: Literature Analysis
Upload a novel → Ask "Who are the main characters?" or "What is the major conflict?"

### Example 2: Research Papers
Upload academic papers → Ask "What is the methodology?" or "What are the key findings?"

### Example 3: Legal Documents
Upload contracts → Ask "What are the payment terms?" or "What are the termination clauses?"

## 🛠️ Development

### Add Custom LLM Models

Edit `rag.py`:
```python
llm = ChatOllama(
    model="your-model-name",  # Change this
    temperature=0.3,
    ...
)
```

Available models: `ollama pull <model-name>`

### Extend Retrieval Strategy

Edit `retriever.py` to use different search types:
```python
search_type="mmr"  # Maximum Marginal Relevance
# or "similarity" (default)
```

### Customize Prompt Template

Edit the template in `rag.py` to change response behavior:
```python
template = """Your custom system prompt here..."""
```

## 📋 Requirements Explained

| Package | Purpose |
|---------|---------|
| `langchain` | Core LLM framework |
| `langchain-community` | Community integrations |
| `langchain-chroma` | ChromaDB integration |
| `langchain-ollama` | Ollama LLM/embeddings |
| `chromadb` | Vector database |
| `pypdf` | PDF reading |
| `streamlit` | Web UI framework |
| `python-dotenv` | Environment variables |
| `tiktoken` | Token counting |
| `langchain-text-splitters` | Document chunking |

## 🚀 Deployment

### Local Network Access

Share with others on your network:
```bash
streamlit run app.py --server.address=0.0.0.0
```

Then access from another machine: `http://<your-ip>:8501`

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t rag-app .
docker run -p 8501:8501 rag-app
```

## 📝 Notes

- **Data Privacy**: Everything runs locally. Documents never leave your machine.
- **Vector Database**: Stored in `chroma_db/`. Delete this folder to reset the database.
- **Model Size**: `nomic-embed-text` (~274MB), `llama3.2` (~2GB+) — requires disk space
- **Performance**: First query may take longer as models load into memory

## 🐛 Known Issues

- Large PDFs (100+ pages) may take time to process
- Complex document layouts might not extract perfectly
- Responses are limited by context window (8192 tokens)

## 🔮 Future Enhancements

- [ ] Support for other document formats (DOCX, TXT, Images)
- [ ] Advanced query types (filtering, metadata search)
- [ ] Multi-language support
- [ ] Custom vector database options
- [ ] Response quality evaluation metrics
- [ ] API endpoint for external integration
- [ ] Streaming responses for faster feedback

## 📞 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Verify Ollama models are installed: `ollama list`
3. Check logs in the terminal running Streamlit
4. Review `requirements.txt` compatibility

## 📄 License

This project is open source. Feel free to modify and use as needed.

---
