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


def chunk_with_langchain_nltk(
    pages: List[str],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Sentence-aware chunking (char-based size + overlap).
    """
    splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    full_text = "\n\n".join(pages)
    return splitter.split_text(full_text)



if __name__ == "__main__":
    # === Replace with your two PDF paths ===
    pdf_paths = ["data/pg_handbook.pdf", "data/ug_handbook.pdf"]
    for p in pdf_paths:
        assert Path(p).exists(), f"PDF not found: {p}"

    # 1) Load both PDFs
    page_texts = load_pdfs(pdf_paths)

    # 2) LangChain + NLTK splitter
    lc_chunks = chunk_with_langchain_nltk(
        page_texts,
        chunk_size=1000,
        chunk_overlap=200,
    )
    print(f"[LangChain NLTK] {len(lc_chunks)} chunks across both PDFs.\n")
    for i, ch in enumerate(lc_chunks[5:9], 1):
        print(f"--- Chunk {i}  (len={len(ch)}) ---\n{ch}...\n")
