from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

# Ensure docs folder exists
os.makedirs("docs", exist_ok=True)

@app.get("/")
def home():
    return {"message": "RAG App Running 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully ✅",
        "filename": file.filename
    }