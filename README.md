# Regulatory Analysis Workbench (Compliance Copilot)

This is a small project born out of a personal need to have a simple tool to use an LLM with confidential PDFs.

With this, I wanted to experiment with the concepts of Agentic RAG and a Hybrid Retrieval Engine, using a local LLM to achieve a fully private system.

The result is this, an Agentic-RAG system designed for compliance and regulatory risk analysis. It automates the process of extracting, searching, and analyzing complex regulatory documents (like DORA or MiCA) with high precision and transparency.

## Key Functionalities

- **Intelligent Document Ingestion**: Supports PDF and DOCX formats. It performs **Stateful Chunking** to robustly link article numbers with their titles even across different paragraphs.
- **Agentic Reasoning**: Powered by a sophisticated agent loop that uses specialized tools to gather evidence, explore context, and synthesize technical answers.
- **Hybrid Retrieval Engine**: Combines **Dense Retrieval** (BGE-M3 embeddings) with **Sparse Retrieval** (BM25) using **Reciprocal Rank Fusion (RRF)** for maximum accuracy on both semantic and keyword-based queries.
- **Verified Citations**: Automatically extracts exact article numbers, titles, and physical page numbers from the document to provide ironclad evidence for every claim.
- **Technical Transparency**: Displays the full **Chain of Thought (CoT)**, including detailed logs of every tool call (arguments and results) and the agent's internal reasoning.
- **Document Mapping**: Generates an automatic outline (Table of Contents) of the document to help the agent orient itself during the analysis.
- **Anti-Loop & Robustness**: Includes mechanisms to prevent repetitive tool calls and advanced JSON extraction logic to handle various LLM response styles.

## Technical Stack & Techniques

- **Backend**: Python with **FastAPI**.
- **Frontend**: **Streamlit** for a rich, interactive user interface.
- **Vector Store**: **ChromaDB** for persistent and scalable storage of document chunks and embeddings.
- **LLM Integration**: OpenAI-compatible API (via **LM Studio**), supporting models like **DeepSeek-R1-Distill-14B**, **Qwen-2.5-Coder**, and **Llama-3.1**.
- **Embeddings**: **BGE-M3** for state-of-the-art multilingual semantic representation.
- **Hybrid Search**: **BM25Okapi** for keyword matching combined with vector search via **RRF**.
- **Chunking Strategy**: Rule-based segmentation with metadata propagation (article/chapter tracking).
- **Tool Calling**: Native tool-use implementation for recursive search and context exploration.

## Prerequisites

- **Python 3.12+** (managed with `uv`).
- **LM Studio** or any OpenAI-compatible server running locally on port `1234`.
- **Docker & Docker Compose** (for containerized deployment).

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Compliance_Copilot

# Install dependencies using uv
uv sync
```

## Execution

### Local (Manual)

1. **Start the Backend**:
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```

2. **Start the UI**:
   ```bash
   uv run streamlit run ui/main.py
   ```

### Docker (Recommended)

To run the entire system with Docker Compose:

```bash
docker-compose up --build
```

The system will be available at:
- **Frontend**: `http://localhost:8501`
- **Backend API**: `http://localhost:8000`

*Note: The Docker configuration uses `host.docker.internal` to connect to LM Studio running on your host machine.*

3. **Access the application**: Open your browser at `http://localhost:8501`.
