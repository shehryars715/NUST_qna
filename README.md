![Glance-picture](https://github.com/user-attachments/assets/6e40716f-7055-4f7d-af89-7d3182a0575e)


# NUST NUST QnA System

## Technical Overview

This project implements a sophisticated Retrieval-Augmented Generation (RAG) pipeline for querying institutional knowledge from the National University of Sciences and Technology (NUST). The system processes heterogeneous document sources through advanced NLP techniques, creates dense vector representations using embeddings, and enables precise information retrieval through semantic similarity search. The architecture also incorporates contextual conversation memory.

## Architectural Components

### 1. Data Processing Pipeline
- **Source Document Acquisition**: Scraping of NUST web properties using asynchronous HTTP requests with proper DOM parsing and content extraction
- **PDF Text Extraction**: Parsing of structured PDF documents (NUST Handbook) with layout-aware text reconstruction
- **Semantic Chunking Strategy**: Implementation of content-aware text segmentation using NLTK's discourse analysis capabilities with optimal chunk sizing (1000 tokens).
- **Text Normalization**: Application of Unicode normalization, technical term preservation, and institutional acronym handling

### 2. Embedding & Vector Store (embedding.py)

- **Uses GoogleGenerativeAIEmbeddings (models/embedding-001).**

- **Stores dense vector representations in FAISS.**

- **Persists vector index locally (faiss_index/).**

### 4. Retrieval-Augmented Generation
- **Query Processing**: Input query expansion using synonym generation and acronym resolution specific to academic terminology
- **Semantic Search**: Multi-query retrieval with maximum marginal relevance (MMR) scoring (λ=0.7) to balance relevance and diversity
- **Contextual Augmentation**: Dynamic context window construction with retrieved chunks formatted with metadata attribution

### 5. Generative Component
- **Prompt Engineering**: Structured prompt templates with explicit instructions for context grounding and refusal of extragenerative responses
- **Gemini Pro Integration**: Utilization of the 32k context window model for generation with temperature=0.1 
- **Citation Mechanism**: Automatic attribution of information sources to retrieved document segments

### 6. Conversation Management
- **Implements ConversationalRetrievalChain with:**

- **Conversation buffer memory (last 3 turns)**

- **Custom prompt template enforcing factuality**

- **Retriever (k=3) for context injection**

## Privacy Consideration

The scraping script used for initial data extraction has been excluded via .gitignore to respect the privacy and data access policies of NUST (or the relevant institution). This ensures sensitive scraping logic is not exposed in public repositories and aligns with responsible data handling practices.

## Project Structure 
```
├── data/                      # Raw input data
│   ├── ug_handbook.pdf        # NUST Undergraduate Handbook
│   ├── scrap.json             # JSON from scraped webpages
│
├── output_chunks/             # Processed chunks
│   ├── pdf_chunks.json
│   ├── json_chunks.json
│
├── faiss_index/               # Local FAISS vector store
│
├── chunking.py                # PDF & JSON chunking pipeline
├── embedding.py               # Embedding + FAISS index creation
├── scrap.py                   # Selenium web scraping of NUST pages
├── search.py                  # RAG pipeline with memory & custom prompt
├── app.py                     # Streamlit chatbot app
│
├── requirements.txt           # Python dependencies
├── .env                       # API keys (Google Gemini)
└── README.md                  # Project documentation

```

## Technical Specifications

### Dependencies and Versioning
```
langchain==0.0.346
faiss-cpu==1.7.4
streamlit==1.28.0
google-generativeai==0.3.0
nltk==3.8.1
beautifulsoup4==4.12.2
pypdf==3.15.0
python-dotenv==1.0.0
tiktoken==0.5.1
```
##  Tech Stack

LangChain (RAG pipeline, memory, chains)

Google Gemini (Generative AI) – Embeddings + LLM

FAISS – Vector similarity search

Selenium – Web scraping

NLTK – Tokenization & chunking

Streamlit – Chatbot frontend

## Installation and Deployment

### Environment Configuration
```bash
# Create conda environment
conda create -n nust-rag python=3.10
conda activate nust-rag

# Install core dependencies
pip install -r requirements.txt

# Download NLTK data assets
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Set environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```



### Application Execution
```bash
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

## Limitations and Future Work

### Current Constraints
- Single embedding model without ensemble approach
- Limited cross-lingual support for Urdu queries
- No explicit temporal awareness for policy changes

### Planned Enhancements
- **Multi-modal Expansion**: Incorporation of diagrams and tables from source documents
- **Temporal Reasoning**: Version-aware retrieval for time-sensitive policies
- **Query Understanding**: Better handling of compound and multi-faceted questions
- **Deployment Scaling**: Kubernetes deployment with horizontal pod autoscaling
### License
This project is licensed under the MIT License - see the LICENSE file for details. All NUST institutional data remains property of the National University of Sciences and Technology.

