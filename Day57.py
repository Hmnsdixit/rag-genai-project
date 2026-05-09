import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Page title
st.title("🤖 AI Document Q&A")

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector database
db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# User input
query = st.text_input("Ask a question")

if query:
    docs = db.similarity_search(query)

    context = " ".join([doc.page_content for doc in docs])

    st.subheader("Answer")
    st.write(context)