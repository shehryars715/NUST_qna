from pathlib import Path
from typing import List
import nltk
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import NLTKTextSplitter

# Make sure sentence tokenizer is ready
nltk.download("punkt", quiet=True)


def load_pdfs(pdf_paths: List[str]) -> List[str]:
    all_pages = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()  # Each PDF returns List[Document]
        all_pages.extend([d.page_content for d in docs])
    return all_pages

import json
from typing import List, Dict
import nltk
from pathlib import Path

nltk.download("punkt", quiet=True)


import json
from pathlib import Path
from typing import List, Dict


def chunk_json_documents(data: List[Dict]) -> List[Dict]:
    """
    Treat each JSON item as one chunk without splitting.
    Returns: List[Dict] with title, content, link, chunk_id
    """
    chunks = []
    for i, doc in enumerate(data, 1):
        chunks.append({
            "title": doc.get("title", ""),
            "content": doc.get("content", ""),
            "link": doc.get("link", ""),
            "chunk_id": i
        })
    return chunks




def custom_chunk_with_nltk(pages: List[str], chunk_size: int = 1000) -> List[str]:
    full_text = "\n\n".join(pages)
    sentences = [s.strip() for s in nltk.sent_tokenize(full_text)]

    chunks = []
    current_chunk = []
    current_chunk_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        if current_chunk_length + sentence_length > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_chunk_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_chunk_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Debug prints
    print(f"Total sentences input: {len(sentences)}")
    print(f"Total chunks created: {len(chunks)}")
    total_chunked_sentences = sum(len(nltk.sent_tokenize(c)) for c in chunks)
    print(f"Total sentences in chunks: {total_chunked_sentences}")

    missing_sentences = set(sentences) - set(
        [s for c in chunks for s in nltk.sent_tokenize(c)]
    )
    print(f"Missing sentences count: {len(missing_sentences)}")

    return chunks



if __name__ == "__main__":
    # File paths
    pdf_paths = [Path("data/ug_handbook.pdf")]
    json_path = Path("data/scrap.json")
    output_dir = Path("output_chunks")
    output_dir.mkdir(exist_ok=True)

    # Check PDF existence
    for p in pdf_paths:
        assert p.exists(), f"PDF not found: {p}"
    assert json_path.exists(), f"JSON file not found: {json_path}"

    # --- Process PDF ---
    pdf_text = load_pdfs(pdf_paths)
    pdf_chunks = custom_chunk_with_nltk(pdf_text, chunk_size=2000)

    pdf_output = output_dir / "pdf_chunks.json"
    with pdf_output.open("w", encoding="utf-8") as f:
        json.dump(pdf_chunks, f, ensure_ascii=False, indent=2)
    print(f"[✓] PDF chunks saved to: {pdf_output.resolve()}")

    # --- Process JSON ---
    with json_path.open("r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_chunks = chunk_json_documents(json_data)

    json_output = output_dir / "json_chunks.json"
    with json_output.open("w", encoding="utf-8") as f:
        json.dump(json_chunks, f, ensure_ascii=False, indent=2)
    print(f"[✓] JSON chunks saved to: {json_output.resolve()}")