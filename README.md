# NUST QA System

A Streamlit-based question-answering app that lets you ask questions about a pre-loaded handbook (PDF or TXT) using Google Gemini embeddings and retrieval-augmented generation.

---

## Features

- Upload and process PDF or TXT documents
- Embeds document chunks using Google Gemini embeddings
- Finds the most relevant chunks for each user query
- Uses Gemini LLM to answer questions based on retrieved context
- Chat-style interface with conversation history

---

## Setup

### 1. Clone the repository

```sh
git clone <https://github.com/shehryars715/NUST_qna>
cd <new>
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Add your Google Gemini API key

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Add your document

Place your PDF or TXT file in the `data/` folder and update `DOCUMENT_PATH` in `app.py` if needed.

---

## Running the App

```sh
streamlit run app.py
```

---

## Usage

- Ask questions in the chat input at the bottom.
- The assistant will answer using information from the handbook of NUST provided in the document.

---

## File Structure

- `app.py` — Streamlit UI and chat logic
- `qasystem.py` — Handles retrieval and LLM interaction
- `document_processor.py` — Loads and splits documents, creates vector store
- `data/` — Folder for your document(s)
- `.env` — Your API key (not committed)

---

## Requirements

- Python 3.8+
- Google Gemini API key

---

## Notes

- Only PDF and TXT files are supported by default.
- The app uses FAISS for fast vector search.
- Make sure your API key has access to Gemini models.

---

## License

MIT
