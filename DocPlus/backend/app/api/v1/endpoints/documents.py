from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.services.ocr import process_document

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        return {
            "id": file.filename, 
            "fileId": file.filename, 
            "name": file.filename, 
            "status": "Ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare la salvare: {str(e)}")

@router.post("/analyze/{file_id}")
async def analyze_document(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fișierul nu a fost găsit pe server.")

    try:
        print(f"🚀 Pornim PaddleOCR pentru: {file_id}...")

        result = process_document(file_path)
        
        return {
            "fileId": file_id,
            "text": result["text_plain"], 
            "raw_data": result["ocr_json"] 
        }
        
    except Exception as e:
        print(f"❌ Eroare OCR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Eroare la procesarea AI: {str(e)}")