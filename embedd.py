import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # Gemini embeddings model
    google_api_key=GOOGLE_API_KEY
)

# --- Load JSON files ---
def load_json_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # should be a list of dicts

file1_chunks = load_json_chunks("output_chunks/json_chunks.json")
file2_chunks = load_json_chunks("output_chunks/pdf_chunks.json")

# Merge all chunks
all_chunks = file1_chunks + file2_chunks

# Extract texts
texts = [chunk["text"] for chunk in all_chunks]

# Create FAISS vector store
vectorstore = FAISS.from_texts(texts, embeddings)

# Save FAISS index locally
vectorstore.save_local("faiss_index")

print("✅ FAISS index created and saved!")
