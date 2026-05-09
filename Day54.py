from fastapi import FastAPI, UploadFile, File
import shutil
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

    # Step 1: Read file
    text = read_file(file_path)

    # Step 2: Split into chunks
    chunks = split_text(text)

    return {
        "message": "File processed successfully ✅",
        "total_chunks": len(chunks),
        "sample_chunk": chunks[0] if chunks else "No content"
    }