from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Load FAISS index
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Initialize Gemini model
gemini_model = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

# ✅ Add memory (last 3 exchanges only)
memory = ConversationBufferWindowMemory(
    k=3,
    memory_key="chat_history",
    return_messages=True
)

# ✅ Custom prompt
prompt_template = """You are a chatbot for NUST. 
Use the following retrieved context to answer the question. 
If the answer is not in the context, say you don't know. If there's a link to web in the context saying "visit:" , provide that too. 
Explain the answer a little bit but stay on track. Don't make things up.

Chat history:
{chat_history}

Context:
{context}

Question: {question}
Answer:"""

CUSTOM_PROMPT = PromptTemplate.from_template(prompt_template)

# ✅ Build ConversationalRetrievalChain with custom prompt
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=gemini_model,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT},  # inject custom prompt
    verbose=True
)

# Define query function
def retrieve_and_answer_query(query):
    result = qa_chain.invoke({"question": query})
    return result["answer"]

while True:
    query = input("Enter your question: ")
    response = retrieve_and_answer_query(query)
    print("Response:", response)