import asyncio
import threading
if threading.current_thread().name == "ScriptRunner.scriptThread":
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)



from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

class DocumentProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        api_key = os.getenv("GOOGLE_API_KEY")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001", google_api_key=api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_document(self):
        """Load and process the document based on its type"""
        if self.file_path.endswith('.pdf'):
            return self._load_pdf()
        elif self.file_path.endswith('.txt'):
            return self._load_text_file()
        else:
            raise ValueError("Unsupported file format")
    
    def _load_pdf(self):
        """Extract text from PDF"""
        with open(self.file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    
    def _load_text_file(self):
        """Read text file"""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def create_vector_store(self, text):
        """Create FAISS vector store from document text"""
        chunks = self.text_splitter.split_text(text)
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        return vector_store