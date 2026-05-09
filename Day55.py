from fastapi import FastAPI, UploadFile, File
import shutil
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

app = FastAPI()

os.makedirs("docs", exist_ok=True)

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    return splitter.split_text(text)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = read_file(file_path)
    chunks = split_text(text)

    # ✅ FREE Embeddings (No API key)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ✅ Vector DB
    db = FAISS.from_texts(chunks, embeddings)
    db.save_local("vectorstore")

    return {
        "message": "Embeddings created & stored ✅ (FREE)",
        "chunks": len(chunks)
    }