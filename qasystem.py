import threading
import asyncio

if threading.current_thread().name == "ScriptRunner.scriptThread":
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from document_processor import DocumentProcessor
import os

from dotenv import load_dotenv
load_dotenv()

class QASystem:
    def __init__(self, file_path):
        self.file_path = file_path
        self.processor = DocumentProcessor(file_path)
        api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.7,
            google_api_key=api_key)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = None
        self.retriever = None  # Add retriever attribute

    def initialize(self):
        """Initialize the QA system by processing the document"""
        text = self.processor.load_document()
        vector_store = self.processor.create_vector_store(text)
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 2})  # Set k=2

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            memory=self.memory,
            verbose=True
        )

    def ask_question(self, question):
        """Ask a question and get a response"""
        if not self.qa_chain or not self.retriever:
            raise RuntimeError("QA system not initialized. Call initialize() first.")

        # Retrieve top similar chunk
        docs = self.retriever.get_relevant_documents(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        # Pass the context and question to the LLM
        system_prompt = "You are a helpful assistant for NUST. Answer clearly and concisely.\n"
        prompt = f"{system_prompt}Context:\n{context}\n\nQuestion: {question}"
        result = self.llm.invoke(prompt)
        answer= result.content if hasattr(result, "content") else result
        return answer