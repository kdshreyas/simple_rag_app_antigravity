# Local RAG API

## Setup

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama**
   Download from [ollama.com](https://ollama.com).
   Run the model:
   ```bash
   ollama pull llama3
   ollama serve
   ```
   *Note: You can change the model in `app/core/config.py`.*

3. **Run Server**
   ```bash
   python main.py
   ```

## Usage

1. **Ingest Data**
   Place PDFs/Text files in `data/raw/`.
   Call `POST /api/ingest`.

2. **Query**
   Call `POST /api/query` with JSON `{"query": "your question"}`.
