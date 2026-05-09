from fastapi import FastAPI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

app = FastAPI()

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector DB
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

@app.get("/ask")
def ask_question(query: str):
    # Step 1: Retrieve relevant docs
    docs = db.similarity_search(query)

    # Step 2: Combine context
    context = " ".join([doc.page_content for doc in docs])

    # Step 3: Generate answer (simple)
    return {
        "question": query,
        "answer": context
    }