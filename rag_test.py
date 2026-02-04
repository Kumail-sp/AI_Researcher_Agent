import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma  # This is the updated modern import

# 1. Load your secret key
load_dotenv()

# 2. LOAD: Read the PDF from your 'data' folder
print("--- 📂 Loading PDF ---")
loader = PyPDFLoader("data/knowledge.pdf")
pages = loader.load()

# 3. CHUNK: Break the PDF into smaller pieces (the AI can't read 100 pages at once)
print("--- ✂️ Splitting text into chunks ---")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(pages)

# 4. EMBED & STORE: Turn text into "Vectors" (numbers) and save to ChromaDB
print("--- 💾 Saving to Vector Database ---")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# This creates a folder named 'chroma_db' so you don't have to re-read the PDF every time
vector_db = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

# 5. RETRIEVE: Ask a question about YOUR PDF
query = "What is the summary of this document?"
print(f"--- 🔍 Searching for info about: {query} ---")
docs = vector_db.similarity_search(query, k=2)

# 6. GENERATE: Let the AI answer using ONLY the context from your PDF
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
context = "\n\n".join([doc.page_content for doc in docs])
prompt = f"Use this info to answer: {context}\n\nQuestion: {query}"

response = llm.invoke(prompt)

print("\n--- 🤖 AI ANSWER FROM YOUR PDF ---")
print(response.content)